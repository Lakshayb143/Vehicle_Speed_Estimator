
from utils.logging_util import initialize_logging
from utils.points_utils import get_points




from src.config import settings


"""Intializing logging """
initialize_logging()
logger = logging.getLogger(__name__)


def main():
    """Entry point of the application"""

    logger.info(f"\n\n\n\n")
    logger.info("-------------------------Starting application------------------------------------")


    """
    Defining Homography points
    These points were acquired using 'points_utils.py' for both videos.
    """
    logger.info("Defining Homography points using points_utils.py' for both videos.")
    source_points = np.float32([])



    width, height = 1920, 1080
    destination_points = np.float32([])



if __name__ == "__main__":
    main()