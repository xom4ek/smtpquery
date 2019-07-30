from consumer import Consumer
from email_class import cfg
import logging


LOGGER = logging.getLogger(__name__)
LOG_FORMAT = ("{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}")
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

Consumer(**cfg.rabbit).main()
