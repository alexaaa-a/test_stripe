# Django + Stripe

## 🚀 Функционал
- item/<int:item_id>/ - купить конкретный товар
- payment-intent-page/<int:item_id>/ - купить конкретный товар (intent)
- order-page/ - собрать заказ из доступных товаров и оплатить его
- .env был добавлен для удобства использования
  
---

## 🔧 Локальный запуск:
```bash
git clone <repo>
docker compose up --build
