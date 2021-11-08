
import generator
from database import _setup
from database import Db
from database import _delete_entries_content
import time
import app


# _setup('ski')
# _delete_entries_content()

# g = generator.Generator(1000)
# g.run()

app = app.App()
tim = app.calculate_time()
print(tim)

