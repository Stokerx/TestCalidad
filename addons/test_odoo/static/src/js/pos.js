odoo.define('test_odoo.pos', function(require) {
    "use strict";
    
        const PaymentScreen = require('point_of_sale.PaymentScreen');
        const { useListener } = require("@web/core/utils/hooks");
        const Registries = require('point_of_sale.Registries');
    
        const PaymentScreenInherit = (PaymentScreen) =>
            class extends PaymentScreen {
                setup() {
                    super.setup();
                    useListener('payment-selected', this._paymentSelected);
                }
    
                async _paymentSelected() {
                    var order = this.env.pos.get_order();
                    var orderlines = order.get_orderlines();
                    for (var i = 0; i < orderlines.length; i++) {
                        if (orderlines[i].get_price() <= 0) {
                            this.showPopup('ErrorPopup', {
                                title: this.env._t('Error'),
                                body: this.env._t('No se puede seleccionar un producto con precio 0.0'),
                            });
                            return;
                        }
                    }
                }

                async clickBoleta() {
                    const total = this.env.pos.get_order().get_total_with_tax();
                    this.showPopup('ErrorPopup', { 
                        title: this.env._t('Total a pagar'),
                        body: this.env._t('El monto total es: ') + this.env.pos.format_currency(total),
                    });
                }
            };
    
        Registries.Component.extend(PaymentScreen, PaymentScreenInherit);
        return PaymentScreen;
    });