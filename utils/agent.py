import subprocess
from utils.gitlab_api import post_comment_to_mr, trigger_pipeline

async def review_merge_request(project_id, mr_iid, diff):
    prompt = f"You are a helpful code reviewer. Analyze this code diff and give constructive feedback:\n\n{diff}"

    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        capture_output=True,
        text=True
    )

    comment = result.stdout.strip()
    print("AI Review Output:", comment)
    await post_comment_to_mr(project_id, mr_iid, comment)
    await trigger_pipeline(project_id, "main")
