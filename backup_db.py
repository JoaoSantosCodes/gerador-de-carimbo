import shutil
from datetime import datetime

src = 'carimbos.db'
dst = f'carimbos_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
shutil.copy2(src, dst)
print(f'Backup criado: {dst}') 