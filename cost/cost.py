def int_input(msg):
    while True:
        rv = input(msg)
        try:
            int(rv)
            return int(rv)
        except ValueError:
            print("ERROR: Integer input required! ")
            continue


print("Department cost calculator.")

members = int_input("How many team members work in the department?: ")
member_hours = int_input("How many hours did the team members work alltogether?: ")
leave_hours = int_input("How many hours of leave was used by the department?: ")

TEAM_LEADER_COST = 80 * 25
TEAM_ASSISTANT_COST = 40 * 20

paid_hours = member_hours + leave_hours
total_member_cost = paid_hours * 12.5
team_member_cost = total_member_cost / members
total_department_cost = TEAM_ASSISTANT_COST + TEAM_LEADER_COST + total_member_cost

print(
    f"""
In the past 2 weeks:
    The team leader costed the department: ${TEAM_LEADER_COST}
    The assistant team leader costed the department: ${TEAM_ASSISTANT_COST}
    Each member costed the department: ${team_member_cost}
    The members costed the department ${total_member_cost} alltogether

Overall, it takes ${total_department_cost} to run this department for 2 weeks.
"""
)

