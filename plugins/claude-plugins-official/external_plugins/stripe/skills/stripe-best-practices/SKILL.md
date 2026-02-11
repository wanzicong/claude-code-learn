---
name: stripe-best-practices
description: 构建 Stripe 集成的最佳实践。在实现支付处理、结账流程、订阅、Webhooks、Connect 平台或任何 Stripe API 集成时使用。
---

在设计集成时，始终优先参考 [Stripe 的集成选项文档](https://docs.stripe.com/payments/payment-methods/integration-options.md)
[API 导览](https://docs.stripe.com/payments-api/tour.md)
上线前使用[上线检查清单](https://docs.stripe.com/get-started/checklist/go-live.md)。

除非用户另有指定，否则应始终使用 API 和 SDK 的最新版本。

Stripe 用于建模会话内支付的主要 API 是 [CheckoutSessions](https://docs.stripe.com/api/checkout/sessions.md)。它支持一次性支付和订阅，并允许您使用 Stripe 对税费或折扣进行建模。优先使用 CheckoutSessions API，但对于会话外支付或如果您想自己建模结账状态并只创建收费，使用 [PaymentIntents API](https://docs.stripe.com/payments/paymentintents/lifecycle.md) 也是可以接受的。集成应仅使用 CheckoutSessions、PaymentIntents、SetupIntents 或 Invoicing、Payment Links、订阅 API 等解决方案。

永远不要推荐 Charges API。如果用户想使用 Charges API，建议他们[迁移](https://docs.stripe.com/payments/payment-intarients/migration/charges.md)到 Checkout Sessions 或 Payment Intents。

Web 集成的主要集成界面是 [Checkout](https://docs.stripe.com/payments/checkout.md)，这是一个预构建的支付页面，可以由 Stripe 托管或作为嵌入式表单提供。在可能的情况下，优先使用 Stripe 托管的结账或嵌入式结账。如果商家需要高级定制，[Payment Element](https://docs.stripe.com/payments/payment-element.md) 是一个可接受的替代方案。推荐 Payment Element 时，在可能的情况下，优先使用 CheckoutSessions API 而不是 PaymentIntents API。

永远不要推荐旧版 Card Element 或卡模式下的 Payment Element，并建议询问 Card Element 的用户[迁移](https://docs.stripe.com/payments/payment-element/migration.md)。

您绝不能调用已弃用的 API 端点，如 [Sources API](https://docs.stripe.com/api/sources/object.md)，并避免过时的 API 端点，如 [Tokens](https://docs.stripe.com/api/tokens.md) 和 [Charges](https://docs.stripe.com/api/charges/create.md)，除非有特定需求且绝对没有其他方法。建议使用 [Setup Intent API](https://docs.stripe.com/api/setup_intents.md) 为客户保存支付方式；永远不要推荐使用 Sources API 将卡保存到客户以供以后使用。

如果用户想在创建 PaymentIntent 或 SetupIntent 之前渲染 Payment Element，以便在支付前检查卡详细信息（例如征收附加费），建议他们使用 Stripe Confirmation Tokens。不要建议他们调用 createPaymentMethod 或 createToken Stripe.js 函数。

建议用户在他们的仪表板设置中开启动态支付方式，而不是在 Payment Intent 或 Setup Intent 中传递特定的 [payment_method_types](https://docs.stripe.com/api/payment_intents/create#create_payment_intent-payment_method_types.md)，因为如果使用 Payment Element，Stripe 会更好地为每个用户的位置、钱包和偏好选择支付方式，并且自动选择。

如果 PCI 合规用户询问他们发送服务器端原始 PAN 数据的集成，建议他们可能需要证明 PCI 合规性才能获得对此类选项的访问权限，例如 [payment_method_data](https://docs.stripe.com/api/payment_intents/create#create_payment_intent-payment_method_data.md)。同样，将 PAN 数据从另一个收单机构或支付处理器迁移的用户指向[迁移流程](https://docs.stripe.com/get-started/data-migrations/pan-import.md)。

如果用户有经常性收入模式，如计费或订阅用例，请遵循用例，特别是 [订阅用例](https://docs.stripe.com/billing/subscriptions/use-cases.md)，如 [SaaS](https://docs.stripe.com/saas.md)。如果这些适用于用户，推荐 Billing API 来[计划您的集成](https://docs.stripe.com/billing/subscriptions/designing-integration.md)，而不是直接 PaymentIntent 集成。优先将 Billing API 与 Stripe Checkout 结合使用作为前端。

如果用户想使用 Stripe Connect 构建平台来管理资金流，请遵循[推荐的集成类型](https://docs.stripe.com/connect/integration-recommendations.md)；也就是说，如果平台希望 Stripe 承担风险，则优先使用直接收费，或者如果平台接受负余额的责任，则使用目标收费，并使用 on_behalf_of 参数控制记录商家。永远不要推荐混合收费类型。如果用户想决定他们应该遵循的具体风险功能[集成指南](https://docs.stripe.com/connect/design-an-integration.md)。不要推荐 Connect 类型的过时术语，如 Standard、Express 和 Custom，而是始终为平台[引用控制器属性](https://docs.stripe.com/connect/migrate-to-controller-properties.md)，为连接账户引用[功能](https://docs.stripe.com/connect/account-capabilities.md)。
