# -*- coding:utf-8 -*-

from odoo import http
import json
from odoo.http import Response
from odoo.http import request


class PresupuestoController(http.Controller):

    @http.route('/api/presupuesto', type='http', auth='public', cors='*', csrf=False, methods=['GET'])
    def get_presupuestos(self):
        campos = ['name','puntuacion','clasificacion','generos_ids','director_id','detalles_ids','vista_general','link_trailer']
        presupuestos = http.request.env['presupuesto'].sudo().search_read([],campos)
        return Response(json.dumps(presupuestos), content_type='application/json', status=200)

    @http.route('/api/presupuesto/<int:presupuesto_id>', type='http', auth='public', cors='*', csrf=False,  methods=['GET'])
    def get_presupuesto(self, presupuesto_id, **kwargs):
        campos = ['name', 'puntuacion', 'clasificacion', 'generos_ids', 'director_id', 'detalles_ids', 'vista_general','link_trailer']
        presupuesto = http.request.env['presupuesto'].sudo().search_read([('id', '=', presupuesto_id)],campos)

        if not presupuesto:
            return Response(json.dumps({'error': 'El presupuesto no existe'}), status=404, content_type='application/json')

        generos = http.request.env['genero'].sudo().search_read([])
        generoData = []
        for genero in generos:
            if genero['id'] in presupuesto[0]['generos_ids']:
                generoData.append({"id": genero['id'], "name": genero['name']})

        presupuesto[0]['generos_ids'] = generoData
        return Response(json.dumps(presupuesto), content_type='application/json', status=200)
    @http.route('/api/presupuesto',type='json', auth='public', cors='*', csrf=False, methods=['POST'])
    def create_presupuesto(self, **kwargs):

        request_data = json.loads(http.request.httprequest.data.decode('utf-8'))

        if ('name' not in request_data) or ('clasificacion' not in request_data):
            return {'error': 'Faltan parametros obligatorios'}, 500

        new_presupuesto = http.request.env['presupuesto'].sudo().create(request_data)
        return {'id': new_presupuesto.id, 'name': new_presupuesto.name}, 200

    @http.route('/api/presupuesto/<int:presupuesto_id>', type='json', auth='public', cors='*', csrf=False, methods=['PUT'])
    def update_presupuesto(self, presupuesto_id, **kwargs):
        request_data = json.loads(http.request.httprequest.data.decode('utf-8'))
        presupuesto = http.request.env['presupuesto'].sudo().search([('id', '=', presupuesto_id)])

        if not presupuesto:
            return {'error': 'No existe el presupuesto'}, 404

        if ('name' not in request_data) or ('clasificacion' not in request_data):
            return {'error': 'Faltan parametros obligatorios'}, 500

        presupuesto.write(request_data)
        updated_presupuesto = http.request.env['presupuesto'].browse(presupuesto_id)
        return json.dumps({'id': updated_presupuesto.id, 'name': updated_presupuesto.name}), 200


    @http.route('/api/presupuesto/<int:presupuesto_id>', type='http', auth='public', cors='*', csrf=False, methods=['DELETE'])
    def delete_presupuesto(self, presupuesto_id, **kwargs):
        presupuesto = request.env['presupuesto'].sudo().search([('id', '=', presupuesto_id)])

        if not presupuesto:
            return Response(json.dumps({'error': 'El presupuesto no existe'}), status=404, content_type='application/json')

        presupuesto.unlink()
        return Response(status=204)

    @http.route('/api/generos', type='http', auth='public', cors='*', csrf=False, methods=['GET'])
    def get_generos(self):

        campos = ['name']
        generos = http.request.env['genero'].sudo().search_read([], campos)
        return Response(json.dumps(generos), content_type='application/json', status=200)