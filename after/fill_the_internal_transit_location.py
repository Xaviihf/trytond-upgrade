from trytond.pool import Pool

pool = Pool()
Shipment = pool.get('stock.shipment.internal')
shipments = Shipment.search([('state', 'not in', ['request', 'draft'])])
for shipment in shipments:
    state = shipment.state
    shipment.state = 'draft'
    shipment.internal_transit_location = shipment.transit_location
    shipment.state = state

Shipment.save(shipments)
transaction.commit()
