import requests


# Reusable class for sending requests to the Billy API
class BillyClient:
    def __init__(self, api_token):
        self.apiToken = api_token

    def request(self, method, url, body):
        base_url = 'https://api.billysbilling.com/v2'

        try:
            response = {
                'GET': requests.get(
                    base_url + url,
                    headers={'X-Access-Token': self.apiToken}
                ),
                'POST': requests.post(
                    base_url + url,
                    json=body,
                    headers={'X-Access-Token': self.apiToken}
                ),
            }[method]
            status_code = response.status_code
            raw_body = response.text

            if status_code >= 400:
                raise requests.exceptions.RequestException(
                    '{}: {} failed with {:d} - {}'
                    .format(method, url, status_code, raw_body)
                )

            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            raise e


# Creates a contact. The server replies with a list of contacts and we
# return the id of the first contact of the list
def create_contact(client, organization_id):
    contact = {
        'organizationId': organization_id,
        'name': 'John',
        'countryId': 'DK'
    }
    response = client.request('POST', '/contacts', {'contact': contact})

    return response['contacts'][0]['id']


# Creates a product. The server replies with a list of products and we
# return the id of the first product of the list
def create_product(client, organization_id):
    product = {
        'organizationId': organization_id,
        'name': 'Pens',
        'prices': [{
            'unitPrice': 200,
            'currencyId': 'DKK'
        }]
    }
    response = client.request('POST', '/products', {'product': product})

    return response['products'][0]['id']


# Creates an invoice, the server replies with a list of invoices and we
# return the id of the first invoice of the list
def create_invoice(client, organization_id, contact_id, product_id):
    invoice = {
        'organizationId': organization_id,
        'invoiceNo': 65432,
        'entryDate': '2013-11-14',
        'contactId': contact_id,
        'lines': [{
            'productId': product_id,
            'unitPrice': 200
        }]
    }
    response = client.request('POST', '/invoices', {'invoice': invoice})

    return response['invoices'][0]['id']


# Get id of organization associated with the API token.
def get_organization_id(client):
    response = client.request('GET', '/organization', None)

    return response['organization']['id']


# Gets a invoice by its Id
def get_invoice(client, invoice_id):
    response = client.request('GET', '/invoices', invoice_id)

    return response['invoices'][0]


# def main():
#     client = BillyClient('INSERT ACCESS TOKEN HERE')
#
#     currentOrganizationId = getOrganizationId(client)
#     newContactId = createContact(client, currentOrganizationId)
#     newProductId = createProduct(client, currentOrganizationId)
#     newinvoiceId = createInvoice(client, currentOrganizationId, newContactId, newProductId)
#     newlyCreatedInvoice = get_invoice(client, newinvoiceId)
#
#     print(newlyCreatedInvoice)
#
#
# main()
