from trytond.pool import Pool

pool = Pool()
Mandate = pool.get('account.payment.sepa.mandate')
mandates = Mandate.search([
    ('state', '=', 'validated'),
    ('address', '=', None),
    ])

for mandate in mandates:
    mandate.address = mandate.on_change_party()

Mandate.save(mandates)
