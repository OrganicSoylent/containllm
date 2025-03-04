#!/usr/bin/env python
import sys
import os
from marketing_posts.crew import MarketingPostsCrew
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    car_brand = os.getenv("CAR_BRAND", "DefaultBrand")
    inputs = {
        'customer_domain': 'cars',
        'project_description': """
{car_brand} is an up-and-coming car brand, recognisable by its daring design and strong engine performance. This project is driving innovative marketing ideas that are at the pulse of time and make {car_brand} stand out among the established brands. The customer experience of the whole end-to-end customer journey is the main focus at the moment.

Customer Domain: Car production and sales
Project Overview: Creating a comprehensive marketing campaign to boost awareness and sales of {car_brand} cars.
"""
    }
    MarketingPostsCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'customer_domain': 'cars',
        'project_description': """
{car_brand} is an up-and-coming car brand, recognisable by its daring design and strong engine performance. This project is driving innovative marketing ideas that are at the pulse of time and make {car_brand} stand out among the established brands. The customer experience of the whole end-to-end customer journey is the main focus at the moment.

Customer Domain: Car production and sales
Project Overview: Creating a comprehensive marketing campaign to boost awareness and sales of {car_brand} cars.
"""
    }
    try:
        MarketingPostsCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
