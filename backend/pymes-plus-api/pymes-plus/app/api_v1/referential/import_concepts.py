from flask import request, jsonify, Response
import json
from .. import api
from ...models import ImportConcept
from ...decorators import json, authorize
from ... import session


@api.route('/import_concepts/company/<int:company_id>', methods=['GET'])
def get_import_concepts_bycompany(company_id):
    """
    # /import_concepts/<int:company_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> company_id <br>
    <b>Description:</b> Return all items <br/>
    import_concepts/{company_id} Return according to id <br/>
    <b>Return:</b> JSON format
    """
    response = ImportConcept.get_import_concept_bycompany(company_id)
    return response


@api.route('/import_concepts/<int:import_concept_id>', methods=['GET'])
def get_import_concept(import_concept_id):
    """
    # /import_concepts/<int:import_concept_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> import_concept_id <br>
    <b>Description:</b> Return import_concepts for the given id
    <b>Return:</b> json format
    """
    response = ImportConcept.get_import_concept(import_concept_id)
    return response


@api.route('/import_concepts/search', methods=['GET'])
def get_import_concept_by_search():
    """
    <b>Path:</b> /imports/search <br>
    <b>Methods:</b> GET<br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return the import  for the give an pattern <br>
    """
    ra = request.args.get
    company_id = ra('companyId')
    code = ra('code')
    search = ra('search')
    simple = ra('simple')
    page_size = ra('page_size')
    page_number = ra('page_number')
    by_param = ra('by_param')

    search = '' if search is None else search.strip()
    words = search.split(' ', 1) if not None else None

    kwargs = dict(search=search, words=words, simple=simple,
                  by_param=by_param, company_id=company_id,
                  code=code, page_size=page_size, page_number=page_number )

    response = ImportConcept.search_import_concept(**kwargs)
    return response


@api.route('/import_concepts/', methods=['POST'])
@authorize('importConcepts', 'c')
def post_import_concept():
    """
    # /import_concepts/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new import_concept in the list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = ImportConcept.post_import_concept(data)
    return response


@api.route('/import_concepts/<int:import_concept_id>', methods=['DELETE'])
@authorize('importConcepts', 'd')
def delete_import_concept(import_concept_id):
    """
    # /import_concepts/<int:import_concept_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> import_concept_id <br>
    <b>Description:</b> Delete a import_concept in list import_concepts<br/>
    <b>Return:</b> json format
    """
    response = ImportConcept.delete_import_concept(import_concept_id)
    return response


@api.route('/import_concepts/<int:import_concept_id>', methods=['PUT'])
@authorize('importConcepts', 'u')
def put_import_concept(import_concept_id):
    """
    # /import_concepts/<int:import_concept_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> import_concept_id <br>
    <b>Description:</b>  Update import_concept in list and return list<br/>
    <b>Return:</b> json format
    """
    data = request.json
    response = ImportConcept.put_import_concept(import_concept_id, data)
    return response
