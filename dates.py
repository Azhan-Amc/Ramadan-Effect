from datetime import timedelta
from hijri_converter import Hijri

def ramadan_window(hijri_year):
    start = Hijri(hijri_year, 9, 1).to_gregorian()
    eid = Hijri(hijri_year, 10, 1).to_gregorian()
    end = eid - timedelta(days=1)
    return start, end

if __name__ == "__main__":
    for y in range(1410, 1448):
        print(y, *ramadan_window(y))