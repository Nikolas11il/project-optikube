# בחירת תמונת בסיס - פייתון 3.9
FROM python:3.9-slim

# הגדרת תיקיית העבודה בקונטיינר
WORKDIR /app

# העתקת קובץ requirements
COPY requirements.txt .

# התקנת החבילות הדרושות
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד המקור
COPY app.py .

# חשיפת פורט 8000 לשרת המטריקות של Prometheus
EXPOSE 8000

# הגדרת משתנה סביבה לקביעת מרווח הזמן בין חישובים (בשניות)
ENV CALCULATION_INTERVAL=5

# הפעלת האפליקציה
CMD ["python", "app.py"]

