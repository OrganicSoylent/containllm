#!/usr/bin/env python
import sys
from marketing_posts.crew import MarketingPostsCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'customer_domain': 'cars',
        'project_description': """
CUPRA is an up-and-coming car brand, recognisable by its daring design and strong engine performance. This project is driving innovative marketing ideas that are at the pulse of time and make CUPRA stand out among the established brands. The customer experience of the whole end-to-end customer journey is the main focus at the moment.

Customer Domain: Car production and sales
Project Overview: Creating a comprehensive marketing campaign to boost awareness and sales of CUPRA cars.
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
CUPRA is an up-and-coming car brand, recognisable by its daring design and strong engine performance. This project is driving innovative marketing ideas that are at the pulse of time and make CUPRA stand out among the established brands. The customer experience of the whole end-to-end customer journey is the main focus at the moment.

Customer Domain: Car production and sales
Project Overview: Creating a comprehensive marketing campaign to boost awareness and sales of CUPRA cars.
"""
    }
    try:
        MarketingPostsCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
