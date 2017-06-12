import os
import pytz
from datetime import datetime

from capritools2.tasks import *

#fetch_prices.delay([34, 35])
#price_update_spawner()

fetch_corp_info(1070320653)
fetch_alliance_info(386292982)
fetch_character_info(93417038)
