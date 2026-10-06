import time


# Approximate pricing for the Groq model.
# Keep pricing in one place so it can be updated easily.
INPUT_COST_PER_MILLION = 0.075
OUTPUT_COST_PER_MILLION = 0.30


def calculate_cost(prompt_tokens, completion_tokens):
    """
    Calculate estimated generation cost in USD.
    """

    input_cost = (
        prompt_tokens / 1_000_000
    ) * INPUT_COST_PER_MILLION

    output_cost = (
        completion_tokens / 1_000_000
    ) * OUTPUT_COST_PER_MILLION

    return input_cost + output_cost


def calculate_metrics(response, start_time, end_time):
    """
    Calculate response performance metrics.
    """

    latency = end_time - start_time

    usage = getattr(response, "usage", None)

    if usage:
        prompt_tokens = getattr(
            usage,
            "prompt_tokens",
            0
        )

        completion_tokens = getattr(
            usage,
            "completion_tokens",
            0
        )

        total_tokens = getattr(
            usage,
            "total_tokens",
            0
        )
    else:
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

    estimated_cost = calculate_cost(
        prompt_tokens,
        completion_tokens
    )

    return {
        "latency_seconds": round(latency, 3),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(
            estimated_cost,
            8
        )
    }


def measure_generation(client, model, prompt):

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    end_time = time.perf_counter()

    metrics = calculate_metrics(
        response,
        start_time,
        end_time
    )

    return response, metrics