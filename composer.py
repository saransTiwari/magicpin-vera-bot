def compose(category, merchant, trigger):

    merchant_name = merchant.get(
        "identity",
        {}
    ).get(
        "name",
        "Merchant"
    )

    signals = merchant.get("signals", [])
    trigger_type = trigger.get("kind", "")

    performance = merchant.get("performance", {})
    history = merchant.get("conversation_history", [])

    # Trigger-based opportunities

    if trigger_type == "perf_dip":

        metric = trigger.get(
            "payload",
            {}
        ).get(
            "metric",
            "performance"
        )

        delta = trigger.get(
            "payload",
            {}
        ).get(
            "delta_pct",
            0
        )

        current_value = performance.get(metric, None)

        if current_value is not None:
            message = (
                f"{merchant_name}, your {metric} dropped by "
                f"{abs(int(delta * 100))}% recently "
                f"(currently {current_value}). "
                f"Would you like me to create a recovery campaign?"
            )
        else:
            message = (
                f"{merchant_name}, your {metric} dropped by "
                f"{abs(int(delta * 100))}% recently. "
                f"Would you like me to create a recovery campaign?"
            )

        return {
            "message": message,
            "cta": "Create campaign",
            "send_as": "VERA",
            "suppression_key": "perf_dip",
            "rationale": "Performance decline detected"
        }

    elif trigger_type == "research_digest":

        if category == "dentists":
            msg = (
                f"{merchant_name}, a new dental research update may help "
                f"high-risk patients. Would you like me to create an "
                f"awareness campaign?"
            )

        elif category == "salons":
            msg = (
                f"{merchant_name}, beauty trend demand is rising. "
                f"Would you like me to create a promotional campaign?"
            )

        elif category == "restaurants":
            msg = (
                f"{merchant_name}, local dining demand is increasing. "
                f"Would you like me to launch a customer campaign?"
            )

        elif category == "gyms":
            msg = (
                f"{merchant_name}, fitness enrollment interest is growing. "
                f"Would you like me to promote a trial offer?"
            )

        elif category == "pharmacies":
            msg = (
                f"{merchant_name}, new healthcare guidance may be relevant "
                f"to repeat customers. Would you like a customer awareness campaign?"
            )

        else:
            msg = (
                f"{merchant_name}, a new industry research update is available. "
                f"Would you like me to create a campaign?"
            )

        return {
            "message": msg,
            "cta": "Create campaign",
            "send_as": "VERA",
            "suppression_key": "research_digest",
            "rationale": "Research-based engagement opportunity"
        }

    elif trigger_type == "recall_due":

        return {
            "message": f"{merchant_name}, several customers may be due for a follow-up. Would you like me to send reminders?",
            "cta": "Send reminders",
            "send_as": "VERA",
            "suppression_key": "recall_due",
            "rationale": "Customer retention opportunity"
        }

    elif trigger_type == "renewal_due":

        days = trigger.get(
            "payload",
            {}
        ).get(
            "days_remaining",
            0
        )

        return {
            "message": f"{merchant_name}, your subscription expires in {days} days. Would you like me to renew it for you?",
            "cta": "Renew now",
            "send_as": "VERA",
            "suppression_key": "renewal_due",
            "rationale": "Subscription renewal reminder"
        }

    elif trigger_type == "regulation_change":

        return {
            "message": f"{merchant_name}, a new regulatory update may affect your practice. Would you like a quick summary?",
            "cta": "View update",
            "send_as": "VERA",
            "suppression_key": "regulation_change",
            "rationale": "Compliance opportunity"
        }

    # Merchant signals

    elif "perf_dip_severe" in signals:

        return {
            "message": f"{merchant_name}, your business performance has dropped recently. Would you like me to create a campaign to bring customers back?",
            "cta": "Create campaign",
            "send_as": "VERA",
            "suppression_key": "perf_dip",
            "rationale": "Performance decline detected"
        }

    elif "no_active_offers" in signals:

        return {
            "message": f"{merchant_name}, you currently have no active offers. Should I create a new customer offer for you today?",
            "cta": "Create offer",
            "send_as": "VERA",
            "suppression_key": "no_offer",
            "rationale": "No active offers available"
        }

    elif "high_risk_adult_cohort" in signals:

        high_risk_count = merchant.get(
            "customer_aggregate",
            {}
        ).get(
            "high_risk_adult_count",
            0
        )

        return {
            "message": f"{merchant_name}, {high_risk_count} high-risk patients may benefit from preventive care outreach. Would you like me to create an awareness campaign?",
            "cta": "Create campaign",
            "send_as": "VERA",
            "suppression_key": "high_risk",
            "rationale": "Patient outreach opportunity"
        }

    elif any("stale_posts" in signal for signal in signals):

        stale_days = 0

        for signal in signals:
            if signal.startswith("stale_posts:"):
                stale_days = signal.split(":")[1].replace("d", "")
                break

        focus_area = ""

        for item in reversed(history):
            body = item.get("body", "").lower()

            if "whitening" in body or "aligners" in body:
                focus_area = " focused on whitening and aligners"
                break

        return {
            "message": f"{merchant_name}, your last post was {stale_days} days ago. Would you like me to create 3 fresh posts this week{focus_area}?",
            "cta": "Create content",
            "send_as": "VERA",
            "suppression_key": "stale_posts",
            "rationale": "Content has not been updated recently"
        }

    return {
        "message": f"{merchant_name}, I found an opportunity to improve engagement today.",
        "cta": "Show suggestion",
        "send_as": "VERA",
        "suppression_key": "default",
        "rationale": "General recommendation"
    }