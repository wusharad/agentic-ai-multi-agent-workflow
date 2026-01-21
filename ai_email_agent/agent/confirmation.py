# Human confirmation
def confirm_action(data: dict) -> bool:
    """
    Ask human for confirmation before executing email action.
    Returns True if approved, False otherwise.
    """

    print("\n📨 Email Action Confirmation")
    print("----------------------------")
    print(f"To       : {data['recipient_email']}")
    print(f"Subject  : {data['subject']}")
    print(f"Body     : {data['body']}")
    print(f"Action   : {data['action']}")

    if data["action"] == "SCHEDULE":
        print(f"Send Time: {data['send_time']}")

    print("----------------------------")

    choice = input("Approve this action? (yes/no): ").strip().lower()

    return choice in ("yes", "y")
