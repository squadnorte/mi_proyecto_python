from django.shortcuts import render, redirect, get_object_or_404
from .models import HabilitadoresIniciativaCabecera, HabilitadoresIniciativaDetalle
from .forms import HabilitadoresIniciativaCabeceraForm, HabilitadoresIniciativaDetalleForm
from habilitadores.models import HabilitadorCiberseguridad
from parametria.models import Parametro
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl
from reportlab.lib.enums import TA_JUSTIFY
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from jira import JIRA
from django.conf import settings
from itsdangerous import URLSafeSerializer
from mi_proyecto.validators import validar_palabras_reservadas_y_caracteres
from django.core.exceptions import ValidationError

# Configurar el serializador con una clave secreta de settings.py
serializer = URLSafeSerializer(settings.ITS_DANGEROUS_SECRET_KEY)

# Funciones para generar y verificar IDs cifrados
def generar_id_cifrado(id):
    return serializer.dumps(id)

def verificar_id_cifrado(token):
    try:
        return serializer.loads(token)
    except:
        return None

@login_required
def listar_iniciativas(request):
    iniciativas = HabilitadoresIniciativaCabecera.objects.filter(estado_auditoria='activo')
    iniciativas_cifradas = [
        {
            'iniciativa': iniciativa,
            'id_cifrado': generar_id_cifrado(iniciativa.pk)
        }
        for iniciativa in iniciativas
    ]
    return render(request, 'habilitadores_iniciativa/listar_iniciativas.html', {'iniciativas': iniciativas_cifradas})

@login_required
def crear_iniciativa(request):
    if request.method == 'POST':
        form_cabecera = HabilitadoresIniciativaCabeceraForm(request.POST)
        if form_cabecera.is_valid():
            cabecera = form_cabecera.save(commit=False)
            cabecera.usuario_auditoria = request.user.username
            try:
                estado_activo = Parametro.objects.get(nombre_parametro='ESTADO', valor_parametro='activo')
                cabecera.estado_auditoria = estado_activo
                cabecera.save()
                return redirect('habin:list')
            except Parametro.DoesNotExist:
                messages.error(request, "Error: No se encontró el estado 'ACTIVO' en la tabla Parametro.")
                return redirect('habin:new')
    else:
        form_cabecera = HabilitadoresIniciativaCabeceraForm()
    
    return render(request, 'habilitadores_iniciativa/crear_iniciativa.html', {'form_cabecera': form_cabecera})

@login_required
def editar_iniciativa(request, token):
    # Descifrar el token para obtener el pk
    pk = verificar_id_cifrado(token)
    if pk is None:
        return HttpResponse("Token inválido o expirado", status=400)

    # Obtener la cabecera de la iniciativa
    cabecera = get_object_or_404(HabilitadoresIniciativaCabecera, pk=pk)
    cabecera_form = HabilitadoresIniciativaCabeceraForm(instance=cabecera)

    # Habilitadores ya asignados que están activos
    habilitadores_asignados = HabilitadoresIniciativaDetalle.objects.filter(
        cabecera=cabecera, estado_auditoria='activo'
    )

    # Contar cumplimientos
    cumple_count = habilitadores_asignados.filter(estado_cumplimiento='Cumple').count()
    no_cumple_count = habilitadores_asignados.filter(estado_cumplimiento='No Cumple').count()

    
    # Manejo de búsqueda en habilitadores asignados
    query_assigned = request.POST.get('q_assigned', '')
    if request.method == 'POST':
        if 'searching' in request.POST:
            if query_assigned:
                habilitadores_asignados = habilitadores_asignados.filter(
                    Q(habilitador__titulo__icontains=query_assigned) | Q(habilitador__codigo__icontains=query_assigned)
                )    

    # Paginación para habilitadores asignados (5 por página)
    paginator_assigned = Paginator(habilitadores_asignados.order_by('habilitador__codigo'), 5)
    page_assigned = request.GET.get('page_assigned')
    habilitadores_asignados_page = paginator_assigned.get_page(page_assigned)

    # Formset para los detalles de los habilitadores asignados
    HabilitadoresIniciativaDetalleFormSet = modelformset_factory(
        HabilitadoresIniciativaDetalle,
        form=HabilitadoresIniciativaDetalleForm,
        extra=0
    )
    detalle_formset = HabilitadoresIniciativaDetalleFormSet(queryset=habilitadores_asignados_page.object_list)

    # Nuevos habilitadores que no están asignados
    habilitadores_asignados_ids = habilitadores_asignados.values_list('habilitador__codigo', flat=True)
    habilitadores_activos = HabilitadorCiberseguridad.objects.filter(
        estado_auditoria__valor_parametro='activo'
    ).exclude(codigo__in=habilitadores_asignados_ids).order_by('codigo')

     # Manejo de búsqueda en nuevos habilitadores
    query_new = request.POST.get('q_new', '')
    if query_new:
        habilitadores_activos = habilitadores_activos.filter(
            Q(titulo__icontains=query_new) | Q(codigo__icontains=query_new)
        )

    # Paginación para nuevos habilitadores (5 por página)
    paginator_new = Paginator(habilitadores_activos, 5)
    page_new = request.GET.get('page_new')
    habilitadores_activos_page = paginator_new.get_page(page_new)

    if request.method == 'POST':
        if 'update_existing' in request.POST:
            # Actualizar habilitadores existentes
            cabecera_form = HabilitadoresIniciativaCabeceraForm(request.POST, instance=cabecera)
            detalle_formset = HabilitadoresIniciativaDetalleFormSet(request.POST, queryset=habilitadores_asignados)

            # Validar los campos de la cabecera y los detalles
            if cabecera_form.is_valid() and detalle_formset.is_valid():
                # Validar campos de la cabecera
                campos_cabecera_a_validar = cabecera_form.cleaned_data.copy()
                for campo, valor in campos_cabecera_a_validar.items():
                    try:
                        validar_palabras_reservadas_y_caracteres(valor)
                    except ValidationError as ve:
                        cabecera_form.add_error(campo, str(ve))

                # Validar campos del detalle
                for form in detalle_formset:
                    if form.cleaned_data:  # Verificar si hay datos limpios
                        campos_detalle_a_validar = form.cleaned_data.copy()
                        for campo, valor in campos_detalle_a_validar.items():
                            try:
                                validar_palabras_reservadas_y_caracteres(valor)
                            except ValidationError as ve:
                                form.add_error(campo, str(ve))

                if not cabecera_form.errors and not any(form.errors for form in detalle_formset):
                    cabecera_form.save()
                    detalle_formset.save()
                    messages.success(request, 'Cabecera y habilitadores actualizados correctamente.')
                    return redirect('habin:edit', token=token)

        elif 'add_new' in request.POST:
            # Agregar nuevos habilitadores
            habilitadores_nuevos = request.POST.getlist('habilitadores')
            for codigo in habilitadores_nuevos:
                habilitador = HabilitadorCiberseguridad.objects.get(codigo=codigo)
                HabilitadoresIniciativaDetalle.objects.create(
                    cabecera=cabecera,
                    habilitador=habilitador,
                    estado_cumplimiento='No Cumple',
                    estado_auditoria='activo',
                    usuario_auditoria=request.user.username
                )
            messages.success(request, 'Nuevos habilitadores agregados correctamente con estado "No Cumple".')
            return redirect('habin:edit', token=token)

    context = {
        'cabecera_form': cabecera_form,
        'detalle_formset': detalle_formset,
        'detalle_formset_page': habilitadores_asignados_page,
        'habilitadores_activos': habilitadores_activos_page,
        'query_assigned': query_assigned,
        'query_new': query_new,
        'cumple_count': cumple_count,
        'no_cumple_count': no_cumple_count,
        'cabecera': cabecera,
        'id_cifrado': cabecera.id_cifrado,
    }

    return render(request, 'habilitadores_iniciativa/editar_iniciativa.html', context)


@login_required
def crear_tarea_jira_api(habilitador):
    # Configuración para conectarse a Jira
    jira_options = {'server': 'https://squadnorte.atlassian.net'}
    try:
        # Autenticación con Jira
        jira = JIRA(options=jira_options, basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN))
        
        # Crear la tarea en Jira con los detalles proporcionados
        issue_dict = {
            'project': {'key': 'SCRUM'},  # Cambia esto por el key de tu proyecto en Jira
            'summary': f'Tarea para habilitador: {habilitador.titulo}',
            'description': f'Detalles del habilitador:\n\nTítulo: {habilitador.titulo}\nDescripción: {habilitador.descripcion}',
            'issuetype': {'name': 'Task'},  # Tipo de tarea en Jira ("Task", "Bug", "Story", etc.)
        }
        new_issue = jira.create_issue(fields=issue_dict)

        # Devuelve la clave o el ID de la tarea creada
        return new_issue.key
    except Exception as e:
        # Imprime el error en los logs (útil para depuración)
        print(f"Error al crear la tarea en Jira: {e}")
        raise

@login_required
def crear_tarea_jira(request, token, habilitador_codigo):
    # Verificar y descifrar el token
    pk = verificar_id_cifrado(token)
    if pk is None:
        messages.error(request, "El token es inválido o ha expirado.")
        return redirect('habin:list')  # Asegúrate de redirigir a una vista adecuada

    # Obtener el habilitador
    habilitador = get_object_or_404(HabilitadorCiberseguridad, codigo=habilitador_codigo)

    # Crear la tarea en Jira
    try:
        tarea_jira = crear_tarea_jira_api(habilitador)
        messages.success(request, f'Tarea creada correctamente: {tarea_jira}')
    except Exception as e:
        messages.error(request, f"Error al crear la tarea en Jira: {str(e)}")

    # Redirigir de vuelta a la vista de edición
    return redirect('habin:edit', token=token)

@login_required
def desasignar_habilitador(request, token):
    # Descifrar el token para obtener el pk
    pk = verificar_id_cifrado(token)
    if pk is None:
        return HttpResponse("Token inválido o expirado", status=400)

    # Obtener el habilitador de detalle usando el pk
    detalle_habilitador = get_object_or_404(HabilitadoresIniciativaDetalle, pk=pk)
    
    # Cambiar el estado_auditoria a 'inactivo'
    detalle_habilitador.estado_auditoria = 'inactivo'
    detalle_habilitador.save()

    # Mensaje de éxito
    messages.success(request, 'Habilitador desasignado correctamente.')

    # Redirigir utilizando el token de la cabecera
    return redirect('habin:edit', token=generar_id_cifrado(detalle_habilitador.cabecera.pk))

@login_required
def generar_reporte_iniciativas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_iniciativas.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    elements = []
    stylesheet = getSampleStyleSheet()
    justified_style = stylesheet['BodyText']
    justified_style.alignment = TA_JUSTIFY
    title = Paragraph("Reporte de Iniciativas", stylesheet['Title'])
    elements.append(title)
    data = [['Habilitador', 'Dimensión', 'Squad', 'Entregable', 'Estado Cumpl.', 'Cod Excepción', 'Comentarios']]
    iniciativas_detalle = HabilitadoresIniciativaDetalle.objects.select_related('habilitador', 'cabecera')

    for detalle in iniciativas_detalle:
        habilitador = Paragraph(detalle.habilitador.titulo, justified_style)
        dimension = Paragraph(detalle.habilitador.dimension.valor_parametro, justified_style)
        squad = Paragraph(detalle.cabecera.squad, justified_style)
        entregable = Paragraph("Sí" if detalle.habilitador.entregable else "No", justified_style)
        estado_cumplimiento = Paragraph(detalle.estado_cumplimiento, justified_style)
        exception = Paragraph(detalle.exception or "N/A", justified_style)
        observacion = Paragraph(detalle.observacion or "Sin comentarios", justified_style)
        data.append([habilitador, dimension, squad, entregable, estado_cumplimiento, exception, observacion])

    table = Table(data, colWidths=[1.5 * inch, 1.2 * inch, 1 * inch, 1 * inch, 1.2 * inch, 1.2 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    table.hAlign = 'CENTER'
    elements.append(table)
    doc.build(elements)
    return response

@login_required
def exportar_reporte_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Iniciativas"
    headers = ['Habilitador', 'Dimensión', 'Squad', 'Entregable', 'Estado Cumpl.', 'Cod Excepción', 'Comentarios']
    ws.append(headers)
    iniciativas_detalle = HabilitadoresIniciativaDetalle.objects.select_related('habilitador', 'cabecera').filter(estado_auditoria='activo')

    for detalle in iniciativas_detalle:
        habilitador = detalle.habilitador.titulo
        dimension = detalle.habilitador.dimension.valor_parametro
        squad = detalle.cabecera.squad
        entregable = "Sí" if detalle.habilitador.entregable else "No"
        estado_cumplimiento = detalle.estado_cumplimiento
        exception = detalle.exception or "N/A"
        observacion = detalle.observacion or "Sin comentarios"
        ws.append([habilitador, dimension, squad, entregable, estado_cumplimiento, exception, observacion[:30]])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_iniciativas.xlsx'
    wb.save(response)
    return response
