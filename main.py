from dotenv import load_dotenv
load_dotenv()
from app.graph import build_graph
from app.nodes import load_sent_emails

config = {
    "configurable": {"thread_id": "7"},
    "recursion_limit": 50
}

def main():
    app = build_graph()

    initial_state = {
        "maxposts":2,
        "unique_email": load_sent_emails(),
    }
    result = app.invoke(initial_state, config=config)

    print(f"total total_job_scan_output : {len(result["total_job_scan_output"])}")
    print(f"total total_irrelevant : {len(result["total_irrelevant"])}")
    print(f"total total_relevant_jobs : {len(result["total_relevant_jobs"])}")
    print(f"total count_scraped_posts : {result["count_scraped_posts"]}")



if __name__ == "__main__":
    main()