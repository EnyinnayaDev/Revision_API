# Revision_API

# Revision Comparison API

## Setup
```bash
python -m venv myenv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints

### GET /docs/{id}/revisions
Returns all revisions for a document.

Example:
#### GET/dodcs/1/revisions

### GET /compare?from={id}&to={id}
Compares two revisions. Both must exist and belong to the same document.

Example: 
 #### GET/compare?from=1&to=2

Errors:
- 400 — missing `from`/`to`, or revisions belong to different documents
- 404 — document or revision not found

## Tests
```bash
python manage.py test revisions
```
7 tests covering validation and diff correctness (cross-document rejection, missing params, nonexistent IDs, self-compare, diff symmetry).