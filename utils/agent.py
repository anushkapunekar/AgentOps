import subprocess
import os
import logging
import traceback
from utils.gitlab_api import post_comment_to_mr, trigger_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def review_merge_request(project_id, mr_iid, diff, branch="main"):
    """
    Review a merge request using AI and post feedback to GitLab.
    
    Args:
        project_id: GitLab project ID
        mr_iid: Merge request internal ID
        diff: Code diff to review
        branch: Branch name (default: "main")
    """
    try:
        # Print AI review started
        print("=" * 80)
        print("AI review started")
        print("=" * 80)
        logger.info("=" * 80)
        logger.info("STARTING MERGE REQUEST REVIEW")
        logger.info("=" * 80)
        
        # Print project_id, mr_iid, diff
        print(f"Project ID: {project_id}")
        print(f"MR IID: {mr_iid}")
        print(f"Branch: {branch}")
        print(f"Diff length: {len(str(diff))} characters")
        print(f"Diff preview: {str(diff)[:200]}...")
        logger.info(f"Project ID: {project_id}, MR IID: {mr_iid}, Branch: {branch}")
        
        # Get AI model from environment
        ai_model = os.getenv("AI_MODEL", "mistral")
        logger.info(f"Using AI model: {ai_model}")
        print(f"Using AI model: {ai_model}")
        
        # Prepare prompt
        prompt = f"You are a helpful code reviewer. Analyze this code diff and give constructive feedback:\n\n{diff}"
        logger.info(f"Prompt length: {len(prompt)} characters")
        
        # Check if using OpenAI or Ollama
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if openai_api_key and ai_model.startswith("gpt"):
            logger.info("Using OpenAI API")
            print("Using OpenAI API")
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=openai_api_key)
                
                response = await client.chat.completions.create(
                    model=ai_model,
                    messages=[
                        {"role": "system", "content": "You are a professional code reviewer. Provide concise, constructive feedback."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )
                
                comment = response.choices[0].message.content.strip()
                logger.info("OpenAI response received successfully")
                
            except ImportError:
                logger.error("OpenAI package not installed. Falling back to Ollama.")
                print("OpenAI package not installed. Falling back to Ollama.")
                comment = await _call_ollama(ai_model, prompt)
            except Exception as e:
                logger.error(f"OpenAI API error: {e}", exc_info=True)
                print(f"OpenAI API error: {e}")
                comment = await _call_ollama(ai_model, prompt)
        else:
            logger.info("Using Ollama")
            print("Using Ollama")
            comment = await _call_ollama(ai_model, prompt)
        
        # Print response from AI
        print("=" * 80)
        print("Response from AI:")
        print(comment)
        print("=" * 80)
        
        # Log AI response
        logger.info("=" * 80)
        logger.info("AI REVIEW OUTPUT")
        logger.info("=" * 80)
        logger.info(f"Comment length: {len(comment)} characters")
        logger.info(f"Comment preview: {comment[:200]}...")
        print("AI Review Output:", comment)
        
        if not comment:
            logger.warning("AI returned empty comment, skipping post to GitLab")
            print("AI returned empty comment, skipping post to GitLab")
            return
        
        # Post comment to merge request
        logger.info("Posting comment to merge request...")
        print("Posting comment to merge request...")
        try:
            status_code = await post_comment_to_mr(project_id, mr_iid, comment)
            if status_code in [200, 201]:
                logger.info(f"Comment posted successfully (status: {status_code})")
                print(f"Comment posted successfully (status: {status_code})")
            else:
                logger.warning(f"Comment post returned non-success status: {status_code}")
                print(f"Comment post returned non-success status: {status_code}")
        except Exception as e:
            logger.error(f"Error posting comment to MR: {e}", exc_info=True)
            print(f"Error posting comment to MR: {e}")
            print(traceback.format_exc())
            # Don't raise - continue to pipeline trigger
        
        # Trigger pipeline
        logger.info("Triggering pipeline...")
        print("Triggering pipeline...")
        try:
            pipeline_status = await trigger_pipeline(project_id, branch)
            if pipeline_status in [200, 201]:
                logger.info(f"Pipeline triggered successfully (status: {pipeline_status})")
                print(f"Pipeline triggered successfully (status: {pipeline_status})")
            else:
                logger.warning(f"Pipeline trigger returned non-success status: {pipeline_status}")
                print(f"Pipeline trigger returned non-success status: {pipeline_status}")
        except Exception as e:
            logger.error(f"Error triggering pipeline: {e}", exc_info=True)
            print(f"Error triggering pipeline: {e}")
            print(traceback.format_exc())
            # Don't raise - pipeline failure is less critical
        
        logger.info("=" * 80)
        logger.info("MERGE REQUEST REVIEW COMPLETED")
        logger.info("=" * 80)
        print("=" * 80)
        print("MERGE REQUEST REVIEW COMPLETED")
        print("=" * 80)
        
    except Exception as e:
        # Print full exception with traceback
        error_traceback = traceback.format_exc()
        print("=" * 80)
        print("ERROR IN REVIEW_MERGE_REQUEST")
        print("=" * 80)
        print(f"Error: {e}")
        print("Full traceback:")
        print(error_traceback)
        print("=" * 80)
        
        # Log the error
        logger.error("=" * 80)
        logger.error("ERROR IN REVIEW_MERGE_REQUEST")
        logger.error("=" * 80)
        logger.error(f"Error: {e}", exc_info=True)
        
        # Don't raise - log and return to avoid hanging
        return

async def _call_ollama(model: str, prompt: str) -> str:
    """Call Ollama via subprocess."""
    try:
        logger.info(f"Calling Ollama with model: {model}")
        print(f"Calling Ollama with model: {model}")
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        if result.returncode != 0:
            logger.error(f"Ollama subprocess failed with return code {result.returncode}")
            logger.error(f"Stderr: {result.stderr}")
            print(f"Ollama subprocess failed with return code {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return "Error: Failed to get AI review. Please check logs."
        
        comment = result.stdout.strip()
        logger.info("Ollama response received successfully")
        print("Ollama response received successfully")
        return comment
        
    except subprocess.TimeoutExpired:
        logger.error("Ollama subprocess timed out after 120 seconds")
        print("Ollama subprocess timed out after 120 seconds")
        return "Error: AI review timed out. Please try again."
    except FileNotFoundError:
        logger.error("Ollama command not found. Is Ollama installed?")
        print("Ollama command not found. Is Ollama installed?")
        return "Error: Ollama is not installed or not in PATH."
    except Exception as e:
        error_traceback = traceback.format_exc()
        logger.error(f"Error calling Ollama: {e}", exc_info=True)
        print(f"Error calling Ollama: {e}")
        print("Full traceback:")
        print(error_traceback)
        return f"Error: {str(e)}"
