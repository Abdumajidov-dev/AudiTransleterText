2. Docker bilan ishga tushirish

```bash
# Barcha servislarni ishga tushirish
docker-compose up -d

# Ma'lumotlar bazasini migrate qilish
docker-compose exec backend alembic upgrade head
```