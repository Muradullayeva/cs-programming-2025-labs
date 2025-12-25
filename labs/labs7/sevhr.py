#1
objects = [
    ("Containment Cell A", 4),
    ("Archive Vault", 1),
    ("Bio Lab Sector", 3),
    ("Observation Wing", 2)
]

sorted_objects = sorted(objects, key=lambda x: x[1])

print("Объекты, отсортированные по уровню угрозы:")
for obj in sorted_objects:
    print(f"{obj[0]} - Уровень угрозы: {obj[1]}")

#2
staff_shifts = [
    {"name": "Dr. Shaw", "shift_cost": 120, "shifts": 15},
    {"name": "Agent Torres", "shift_cost": 90, "shifts": 22},
    {"name": "Researcher Hall", "shift_cost": 150, "shifts": 10}
]

total_costs = list(map(lambda emp: {
    "name": emp["name"],
    "total_cost": emp["shift_cost"] * emp["shifts"]
}, staff_shifts))

max_cost_info = max(total_costs, key=lambda x: x["total_cost"])

print("Общая стоимость работы каждого сотрудника:")
for cost in total_costs:
    print(f"{cost['name']}: ${cost['total_cost']}")

print(f"\nМаксимальная стоимость: {max_cost_info['name']} - ${max_cost_info['total_cost']}")

#3
personnel = [
    {"name": "Dr. Klein", "clearance": 2},
    {"name": "Agent Brooks", "clearance": 4},
    {"name": "Technician Reed", "clearance": 1}
]

personnel_with_category = list(map(lambda p: {
    "name": p["name"],
    "clearance": p["clearance"],
    "category": (
        "Restricted" if p["clearance"] == 1 else
        "Confidential" if 2 <= p["clearance"] <= 3 else
        "Top Secret"
    )
}, personnel))

print("Персонал с категориями допуска:")
for person in personnel_with_category:
    print(f"{person['name']}: Уровень {person['clearance']} - {person['category']}")

#4
zones = [
    {"zone": "Sector-12", "active_from": 8, "active_to": 18},
    {"zone": "Deep Storage", "active_from": 0, "active_to": 24},
    {"zone": "Research Wing", "active_from": 9, "active_to": 17}
]

daytime_zones = list(filter(
    lambda z: z["active_from"] >= 8 and z["active_to"] <= 18,
    zones
))

print("Зоны, работающие в дневной период (8:00-18:00):")
for zone in daytime_zones:
    print(f"{zone['zone']}: с {zone['active_from']}:00 до {zone['active_to']}:00")

#5

reports = [
    {"author": "Dr. Moss", "text": "Analysis completed. Reference: http://external-archive.net"},
    {"author": "Agent Lee", "text": "Incident resolved without escalation."},
    {"author": "Dr. Patel", "text": "Supplementary data available at https://secure-research.org"},
    {"author": "Supervisor Kane", "text": "No anomalies detected during inspection."},
    {"author": "Researcher Bloom", "text": "Extended observations uploaded to http://research-notes.lab"},
    {"author": "Agent Novak", "text": "Perimeter secured. No external interference observed."},
    {"author": "Dr. Hargreeve", "text": "Full containment log stored at https://internal-db.scp"},
    {"author": "Technician Moore", "text": "Routine maintenance completed successfully."},
    {"author": "Dr. Alvarez", "text": "Cross-reference materials: http://crosslink.foundation"},
    {"author": "Security Officer Tan", "text": "Shift completed without incidents."},
    {"author": "Analyst Wright", "text": "Statistical model published at https://analysis-hub.org"},
    {"author": "Dr. Kowalski", "text": "Behavioral deviations documented internally."},
    {"author": "Agent Fischer", "text": "Additional footage archived: http://video-storage.sec"},
    {"author": "Senior Researcher Hall", "text": "All test results verified and approved."},
    {"author": "Operations Lead Grant", "text": "Emergency protocol draft shared via https://ops-share.scp"}
]

reports_with_links = list(filter(
    lambda r: 'http://' in r['text'] or 'https://' in r['text'],
    reports
))

import re

cleaned_reports = list(map(
    lambda r: {
        "author": r["author"],
        "text": re.sub(r'https?://[^\s]+', '[ДАННЫЕ УДАЛЕНЫ]', r["text"])
    },
    reports_with_links
))

print("Отчеты, содержавшие ссылки (после очистки):")
print("=" * 50)
for report in cleaned_reports:
    print(f"Автор: {report['author']}")
    print(f"Текст: {report['text']}")
    print("-" * 50)

#6
scp_objects = [
    {"scp": "SCP-096", "class": "Euclid"},
    {"scp": "SCP-173", "class": "Euclid"},
    {"scp": "SCP-055", "class": "Keter"},
    {"scp": "SCP-999", "class": "Safe"},
    {"scp": "SCP-3001", "class": "Keter"}
]

# Фильтрация SCP-объектов, требующих усиленных мер содержания
enhanced_containment_scps = list(filter(
    lambda scp: scp["class"] != "Safe",
    scp_objects
))

print("SCP-объекты, требующие усиленных мер содержания:")
for scp in enhanced_containment_scps:
    print(f"{scp['scp']} - Класс: {scp['class']}")

#7
incidents = [
    {"id": 101, "staff": 4},
    {"id": 102, "staff": 12},
    {"id": 103, "staff": 7},
    {"id": 104, "staff": 20}
]

sorted_incidents = sorted(
    incidents,
    key=lambda x: x["staff"],
    reverse=True
)

top_3_incidents = sorted_incidents[:3]

print("Три наиболее ресурсоемких инцидента:")
for incident in top_3_incidents:
    print(f"Инцидент ID: {incident['id']} - Персонал: {incident['staff']} чел.")

#8
protocols = [
    ("Lockdown", 5),
    ("Evacuation", 4),
    ("Data Wipe", 3),
    ("Routine Scan", 1)
]

formatted_protocols = list(map(
    lambda p: f"Protocol {p[0]} - Criticality {p[1]}",
    protocols
))

print("Протоколы безопасности:")
for protocol in formatted_protocols:
    print(protocol)

#9
shifts = [6, 12, 8, 24, 10, 4]

valid_shifts = list(filter(
    lambda duration: 8 <= duration <= 12,
    shifts
))

print(f"Все смены: {shifts}")
print(f"Смены длительностью от 8 до 12 часов: {valid_shifts}")

#10

evaluations = [
    {"name": "Agent Cole", "score": 78},
    {"name": "Dr. Weiss", "score": 92},
    {"name": "Technician Moore", "score": 61},
    {"name": "Researcher Lin", "score": 88}
]

# Поиск сотрудника с наивысшей оценкой
top_performer = max(
    evaluations,
    key=lambda x: x["score"]
)

print(f"Сотрудник с наивысшей оценкой: {top_performer['name']}")
print(f"Балл: {top_performer['score']}")

