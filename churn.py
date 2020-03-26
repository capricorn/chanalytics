import time
from random import randint

import fourchan

# Collect statistics on a board's churn rate (how quickly posts are archived)

print('Initializing..')
catalog = fourchan.get_catalog('pol')
ids = { thread.id for thread in catalog }

# Could setup a churn queue to wait on verification regarding thread status (archived/deleted)
while True:
    time.sleep(10)
    print(f'[{time.time()}] Checking catalog for update')
    catalog = fourchan.get_catalog('pol')
    new_ids = { thread.id for thread in catalog }

    # Would be better to verify that the thread was archived, and not just removed.
    if new_ids != ids:
        archived_threads = ids - new_ids
        with open('churn.csv', 'a+') as f:
            [ f.write(f'{time.time()},{thread}\n') for thread in archived_threads ]
            print(f'Recorded {len(archived_threads)} churns ({archived_threads})')
        ids = new_ids
