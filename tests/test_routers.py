from app.routers import route_next


def test_job_with_email_goes_to_send_email():
    state = {
        "job_count": 1,
        "relevant_jobs": [
            {"is_positive_email": False},
            {"is_positive_email": True},
        ],
        "count_scraped_posts": 1,
        "total_scraped_posts": 3,
    }
    assert route_next(state) == "send_email"


def test_job_without_email_goes_to_others():
    state = {
        "job_count": 0,
        "relevant_jobs": [{"is_positive_email": False}],
        "count_scraped_posts": 1,
        "total_scraped_posts": 3,
    }
    assert route_next(state) == "others"


def test_no_jobs_left_and_more_posts_scans_next_post():
    state = {
        "job_count": 1,
        "relevant_jobs": [{"is_positive_email": True}],
        "count_scraped_posts": 1,
        "total_scraped_posts": 3,
    }
    assert route_next(state) == "scan_next_post"


def test_no_jobs_left_and_no_more_posts_ends():
    state = {
        "job_count": 1,
        "relevant_jobs": [{"is_positive_email": True}],
        "count_scraped_posts": 3,
        "total_scraped_posts": 3,
    }
    assert route_next(state) == "end"