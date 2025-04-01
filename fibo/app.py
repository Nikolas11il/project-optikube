import random
import time
import sys
import os
import uuid
from functools import lru_cache
from prometheus_client import start_http_server, Gauge

# זמן ריצה - המטריקה היחידה שאנחנו חושפים
# משתמשים ב-labelnames כדי להגדיר משתנה ייחודי לכל ריצה
EXECUTION_TIME = Gauge('fibonacci_execution_time_seconds', 'זמן הריצה של חישוב פיבונאצ\'י', 
                       ['run_id', 'fibonacci_n'])

# פונקציית פיבונאצ'י עם מטמון
@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def calculate_fibonacci(n, run_id):
    # מדידת זמן הריצה
    start_time = time.time()
    
    # חישוב ערך פיבונאצ'י
    result = fibonacci(n)
    
    # חישוב זמן הריצה הכולל
    execution_time = time.time() - start_time
    
    # עדכון המטריקה עם ה-run_id והמספר שחושב
    EXECUTION_TIME.labels(run_id=run_id, fibonacci_n=str(n)).set(execution_time)
    
    return result, execution_time

def main():
    # קריאת משתנה סביבה למרווח הזמן בין חישובים
    calculation_interval = int(os.environ.get('CALCULATION_INTERVAL', 5))
    
    # התחלת שרת מטריקות של Prometheus
    start_http_server(8001)
    print(f"שרת מטריקות Prometheus פועל בפורט 8000")
    print(f"מרווח זמן בין חישובים: {calculation_interval} שניות")
    print(f"חושף מטריקה: fibonacci_execution_time_seconds עם משתנה ייחודי לכל ריצה")
    
    try:
        while True:
            # יצירת מזהה ייחודי לריצה הנוכחית
            run_id = str(uuid.uuid4())
            
            # הגרלת מספר בין 10 ל-30
            random_num = random.randint(100, 120)
            
            print(f"ריצה {run_id}: חישוב איבר פיבונאצ'י מספר {random_num}...")
            
            # חישוב פיבונאצ'י עם מדידת זמן
            result, execution_time = calculate_fibonacci(random_num, run_id)
            
            # הדפסת התוצאות והמטריקה
            print(f"האיבר ה-{random_num} בסדרת פיבונאצ'י הוא: {result}")
            print(f"זמן ריצה: {execution_time:.6f} שניות")
            print(f"מזהה ריצה: {run_id}")
            print("-" * 40)
            
            # המתנה לפני האיטרציה הבאה
            time.sleep(calculation_interval)
            
    except KeyboardInterrupt:
        print("\nהתוכנית הופסקה על ידי המשתמש")

if __name__ == "__main__":
    main()
