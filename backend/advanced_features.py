"""
Advanced AI features for HealthPal including nutrition suggestions and health insights
"""

from datetime import datetime, timedelta
import json

# ==================== NUTRITION SUGGESTIONS ====================

def get_nutrition_suggestions(user_profile, health_data):
    """
    Generate personalized nutrition suggestions based on user profile and health data
    """
    suggestions = {
        'breakfast': [],
        'lunch': [],
        'dinner': [],
        'snacks': [],
        'hydration': [],
        'supplements': []
    }
    
    # Age-based suggestions
    age = user_profile.get('age', 30)
    
    # Energy level and health goals
    if health_data.get('stress_level', 5) > 7:
        suggestions['breakfast'].extend([
            "Whole grain toast with avocado (healthy fats for stress relief)",
            "Greek yogurt with berries and honey (probiotics + antioxidants)",
            "Oatmeal with almonds and banana (B vitamins for stress)"
        ])
    
    if health_data.get('exercise_minutes', 0) > 30:
        suggestions['post-exercise'].extend([
            "Chicken with brown rice (protein + carbs for recovery)",
            "Protein smoothie with banana and peanut butter",
            "Tuna sandwich on whole wheat (omega-3 + protein)"
        ])
    
    # Dietary restrictions
    dietary_restrictions = user_profile.get('dietary_restrictions', '')
    if 'vegetarian' in dietary_restrictions.lower():
        suggestions['lunch'].extend([
            "Chickpea curry with quinoa (complete protein)",
            "Lentil soup with whole grain bread (high fiber, protein)",
            "Tofu stir-fry with vegetables (iron-rich)"
        ])
    elif 'vegan' in dietary_restrictions.lower():
        suggestions['lunch'].extend([
            "Buddha bowl with legumes and vegetables",
            "Hummus and vegetable wrap",
            "Black bean and sweet potato tacos"
        ])
    else:
        suggestions['lunch'].extend([
            "Grilled salmon with green vegetables (omega-3)",
            "Lean chicken breast with sweet potato",
            "Turkey meatballs with whole grain pasta"
        ])
    
    # Hydration recommendations
    blood_pressure = user_profile.get('blood_pressure_sys', 120)
    if blood_pressure > 130:
        suggestions['hydration'].append("Increase water intake - aim for 10-12 glasses daily")
        suggestions['hydration'].append("Reduce sodium intake (limit processed foods)")
        suggestions['sodium-free'].extend([
            "Fresh fruits and vegetables",
            "Grilled fish with herbs",
            "Brown rice and beans"
        ])
    
    # Sleep-related nutrition
    sleep_hours = health_data.get('sleep_hours', 7)
    if sleep_hours < 6:
        suggestions['evening'].extend([
            "Chamomile tea with honey",
            "Warm milk with turmeric",
            "Almonds and walnuts (magnesium for sleep)",
            "Avoid caffeine after 2 PM"
        ])
    
    # Weight management
    weight = user_profile.get('weight_kg', 70)
    height = user_profile.get('height_cm', 170)
    bmi = weight / ((height / 100) ** 2) if height > 0 else 0
    
    if bmi > 25:
        suggestions['snacks'].extend([
            "Apple with almond butter",
            "Carrot and celery with hummus",
            "Greek yogurt",
            "Berries"
        ])
        suggestions['general'].append("Focus on whole foods, reduce processed foods")
    elif bmi < 18.5:
        suggestions['snacks'].extend([
            "Trail mix with nuts and dried fruits",
            "Whole grain bread with cheese",
            "Protein-rich smoothies"
        ])
        suggestions['general'].append("Eat nutrient-dense foods, increase portion sizes")
    
    # Allergy considerations
    allergies = user_profile.get('allergies', '')
    if 'nuts' in allergies.lower():
        # Replace nut-based suggestions
        suggestions['snacks'] = [s for s in suggestions['snacks'] if 'nut' not in s.lower()]
        suggestions['snacks'].extend(["Seeds (sunflower, pumpkin)", "Fruit smoothies"])
    
    if 'dairy' in allergies.lower():
        # Replace dairy suggestions
        suggestions['breakfast'] = [s for s in suggestions['breakfast'] if 'yogurt' not in s.lower()]
        suggestions['breakfast'].extend(["Almond milk with granola", "Soy yogurt with fruits"])
    
    # Blood sugar management
    blood_sugar = health_data.get('blood_sugar', 100)
    if blood_sugar > 110:
        suggestions['glucose-management'] = [
            "Low glycemic index foods (oats, beans, legumes)",
            "Pair carbs with protein or fat (slows absorption)",
            "Avoid sugary drinks and processed foods",
            "Regular meal timing",
            "Increase fiber intake (vegetables, whole grains)"
        ]
    
    return suggestions


# ==================== NUTRITION PLAN GENERATOR ====================

def generate_weekly_nutrition_plan(user_profile, health_data):
    """
    Generate a complete weekly meal plan based on user preferences and health needs
    """
    
    meal_plan = {
        'week': datetime.utcnow().isocalendar()[1],
        'days': {}
    }
    
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Base meal templates
    high_protein_meals = [
        {'name': 'Grilled Chicken with Vegetables', 'protein': 35, 'calories': 450},
        {'name': 'Salmon with Sweet Potato', 'protein': 40, 'calories': 500},
        {'name': 'Turkey Meatballs with Pasta', 'protein': 30, 'calories': 480},
        {'name': 'Lean Beef Steak with Broccoli', 'protein': 45, 'calories': 520},
    ]
    
    balanced_meals = [
        {'name': 'Quinoa Bowl with Chickpeas', 'protein': 18, 'calories': 420},
        {'name': 'Brown Rice with Black Beans', 'protein': 15, 'calories': 400},
        {'name': 'Whole Wheat Pasta with Vegetables', 'protein': 12, 'calories': 380},
    ]
    
    healthy_snacks = [
        {'name': 'Greek Yogurt with Berries', 'calories': 150},
        {'name': 'Apple with Almond Butter', 'calories': 180},
        {'name': 'Mixed Nuts', 'calories': 160},
        {'name': 'Carrot Sticks with Hummus', 'calories': 120},
    ]
    
    for idx, day in enumerate(days_of_week):
        meal_plan['days'][day] = {
            'breakfast': {
                'name': 'Oatmeal with Berries and Honey',
                'calories': 300,
                'benefits': 'High fiber, sustained energy'
            },
            'lunch': high_protein_meals[idx % len(high_protein_meals)],
            'dinner': balanced_meals[idx % len(balanced_meals)],
            'snack': healthy_snacks[idx % len(healthy_snacks)],
            'hydration': 8  # glasses of water
        }
    
    return meal_plan


# ==================== HEALTH INSIGHTS ====================

def generate_health_insights(user_id, db, User, HealthCheckIn):
    """
    Generate actionable health insights from user data
    """
    user = User.query.get(user_id)
    
    # Get last 30 days of data
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=30)
    
    checkins = HealthCheckIn.query.filter(
        HealthCheckIn.user_id == user_id,
        HealthCheckIn.check_in_date >= start_date,
        HealthCheckIn.check_in_date <= end_date
    ).all()
    
    insights = {
        'period': f'{start_date} to {end_date}',
        'recommendations': [],
        'warnings': [],
        'achievements': []
    }
    
    if not checkins:
        return insights
    
    # Sleep analysis
    avg_sleep = sum([c.sleep_hours or 0 for c in checkins]) / len(checkins)
    if avg_sleep < user.sleep_goal_hours - 1:
        insights['warnings'].append(f"Your average sleep is {avg_sleep:.1f} hours, below your goal of {user.sleep_goal_hours} hours")
        insights['recommendations'].append("Try a consistent bedtime routine and avoid screens 30 minutes before bed")
    elif avg_sleep >= user.sleep_goal_hours:
        insights['achievements'].append(f"Great job maintaining {avg_sleep:.1f} hours of sleep on average!")
    
    # Water intake
    avg_water = sum([c.water_intake_liters or 0 for c in checkins]) / len(checkins)
    if avg_water < 6:
        insights['warnings'].append(f"Your daily water intake averages {avg_water:.1f} liters (goal: 8)")
        insights['recommendations'].append("Set a timer for water breaks every 2 hours")
    else:
        insights['achievements'].append(f"Excellent hydration - averaging {avg_water:.1f} liters daily!")
    
    # Exercise consistency
    exercise_days = len([c for c in checkins if c.exercise_minutes and c.exercise_minutes > 0])
    if exercise_days < len(checkins) * 0.5:
        insights['warnings'].append(f"You exercised only {exercise_days} days out of {len(checkins)}")
        insights['recommendations'].append("Start with 10-minute walks and gradually increase activity")
    else:
        insights['achievements'].append(f"Great consistency! You exercised {exercise_days} days out of {len(checkins)}")
    
    # Stress management
    avg_stress = sum([c.stress_level or 5 for c in checkins]) / len(checkins)
    if avg_stress > 7:
        insights['warnings'].append(f"Your average stress level is {avg_stress:.1f}/10 (high)")
        insights['recommendations'].append("Practice meditation, deep breathing, or yoga for stress relief")
    
    # Mood patterns
    mood_counts = {}
    for c in checkins:
        if c.mood:
            mood_counts[c.mood] = mood_counts.get(c.mood, 0) + 1
    
    if mood_counts:
        most_common_mood = max(mood_counts, key=mood_counts.get)
        insights['observations'] = {
            'most_common_mood': most_common_mood,
            'mood_distribution': mood_counts
        }
    
    # Medication adherence (if tracked)
    medication_days = len([c for c in checkins if c])  # Assuming medication logged when check-in done
    insights['observations']['data_consistency'] = f"You logged data {medication_days} days out of {len(checkins)}"
    
    return insights


# ==================== PERSONALIZED SCHEDULE GENERATOR ====================

def generate_personalized_daily_schedule(user_profile, health_data):
    """
    Generate AI-personalized daily schedule based on user profile and health needs
    """
    
    schedule = {
        'date': datetime.utcnow().date().isoformat(),
        'activities': []
    }
    
    job_stress = user_profile.get('job_stress_level', 'medium')
    
    # Early morning routine (adjust based on preferences)
    schedule['activities'].append({
        'time': '06:00-06:30',
        'activity': 'Wake up & Meditation',
        'duration_minutes': 30,
        'category': 'mindfulness',
        'description': 'Start your day with mindfulness to reduce stress',
        'priority': 'high' if job_stress == 'high' else 'medium'
    })
    
    schedule['activities'].append({
        'time': '06:30-07:00',
        'activity': 'Morning Exercise',
        'duration_minutes': 30,
        'category': 'exercise',
        'description': f'Complete {user_profile.get("exercise_goal_minutes", 30)} minutes of daily exercise',
        'priority': 'high'
    })
    
    schedule['activities'].append({
        'time': '07:00-08:00',
        'activity': 'Breakfast & Water',
        'duration_minutes': 60,
        'category': 'nutrition',
        'description': 'Eat a healthy breakfast and drink 2 glasses of water',
        'priority': 'high'
    })
    
    # Mid-morning
    schedule['activities'].append({
        'time': '10:30-10:40',
        'activity': 'Water Reminder',
        'duration_minutes': 10,
        'category': 'hydration',
        'description': 'Drink a glass of water',
        'priority': 'medium'
    })
    
    schedule['activities'].append({
        'time': '12:00-13:00',
        'activity': 'Lunch Break',
        'duration_minutes': 60,
        'category': 'nutrition',
        'description': 'Healthy lunch with vegetables and protein',
        'priority': 'high'
    })
    
    # Afternoon
    schedule['activities'].append({
        'time': '15:00-15:10',
        'activity': 'Screen Break',
        'duration_minutes': 10,
        'category': 'break',
        'description': 'Look away from screen, stretch, walk around',
        'priority': 'medium'
    })
    
    schedule['activities'].append({
        'time': '15:10-15:15',
        'activity': 'Water & Snack',
        'duration_minutes': 5,
        'category': 'nutrition',
        'description': 'Healthy snack and water',
        'priority': 'medium'
    })
    
    # Evening
    schedule['activities'].append({
        'time': '18:00-19:00',
        'activity': 'Dinner',
        'duration_minutes': 60,
        'category': 'nutrition',
        'description': 'Balanced dinner with vegetables',
        'priority': 'high'
    })
    
    # Check menstrual cycle if applicable
    if user_profile.get('has_menstrual_cycle'):
        cycle_day = user_profile.get('menstrual_cycle_day', 1)
        if 1 <= cycle_day <= 5:
            schedule['activities'].append({
                'time': '19:30-20:00',
                'activity': 'Light Yoga/Stretching',
                'duration_minutes': 30,
                'category': 'exercise',
                'description': 'Gentle yoga to ease menstrual discomfort',
                'priority': 'high'
            })
    
    # Evening routine
    schedule['activities'].append({
        'time': '20:30-21:00',
        'activity': 'Meditation/Relaxation',
        'duration_minutes': 30,
        'category': 'mindfulness',
        'description': 'Wind down with meditation or relaxation techniques',
        'priority': 'high'
    })
    
    schedule['activities'].append({
        'time': '21:00-22:00',
        'activity': 'Evening Routine',
        'duration_minutes': 60,
        'category': 'sleep',
        'description': f'Prepare for {user_profile.get("sleep_goal_hours", 8)} hours of sleep',
        'priority': 'high'
    })
    
    schedule['activities'].append({
        'time': '22:00',
        'activity': 'Sleep',
        'duration_minutes': int(user_profile.get('sleep_goal_hours', 8) * 60),
        'category': 'sleep',
        'description': 'Quality sleep for health and recovery',
        'priority': 'high'
    })
    
    # Summary
    schedule['summary'] = {
        'total_water': 8,
        'total_exercise_minutes': user_profile.get('exercise_goal_minutes', 30),
        'total_meditation_minutes': 60,
        'meals': 3,
        'recommended_sleep_hours': user_profile.get('sleep_goal_hours', 8)
    }
    
    return schedule


# ==================== HEALTH GOAL RECOMMENDATIONS ====================

def get_personalized_health_goals(user_profile, current_health_status):
    """
    Get personalized health goals based on profile and current status
    """
    
    goals = []
    
    # Sleep goals
    goals.append({
        'category': 'sleep',
        'current': current_health_status.get('current_sleep', 0),
        'target': user_profile.get('sleep_goal_hours', 8),
        'unit': 'hours',
        'difficulty': 'medium',
        'tips': [
            'Maintain consistent sleep schedule',
            'Avoid screens 1 hour before bed',
            'Keep bedroom cool and dark',
            'Try relaxation techniques'
        ]
    })
    
    # Water intake
    goals.append({
        'category': 'hydration',
        'current': current_health_status.get('water_today', 0),
        'target': 8,
        'unit': 'liters',
        'difficulty': 'easy',
        'tips': [
            'Drink water with every meal',
            'Keep a water bottle with you',
            'Set phone reminders',
            'Drink warm water in winter'
        ]
    })
    
    # Exercise
    goals.append({
        'category': 'exercise',
        'current': current_health_status.get('exercise_today', 0),
        'target': user_profile.get('exercise_goal_minutes', 30),
        'unit': 'minutes',
        'difficulty': 'medium',
        'tips': [
            'Start with 10-minute walks',
            'Find activities you enjoy',
            'Exercise with friends for motivation',
            'Schedule it like an appointment'
        ]
    })
    
    # Meditation
    goals.append({
        'category': 'meditation',
        'current': current_health_status.get('meditation_today', 0),
        'target': 10,
        'unit': 'minutes',
        'difficulty': 'easy',
        'tips': [
            'Use guided meditation apps',
            'Start with 5 minutes',
            'Find a quiet space',
            'Practice at the same time daily'
        ]
    })
    
    # Medication adherence
    if user_profile.get('medications'):
        goals.append({
            'category': 'medications',
            'current': 0,
            'target': len(user_profile.get('medications', [])),
            'unit': 'pills',
            'difficulty': 'high',
            'tips': [
                'Use a pill organizer',
                'Set phone reminders',
                'Take medication with meals',
                'Keep a medication log'
            ]
        })
    
    # Stress management (if high stress)
    if user_profile.get('job_stress_level') == 'high':
        goals.append({
            'category': 'stress_management',
            'current': 0,
            'target': 60,
            'unit': 'minutes/relaxation',
            'difficulty': 'hard',
            'tips': [
                'Practice deep breathing',
                'Regular meditation',
                'Yoga or stretching',
                'Talk to someone you trust',
                'Take breaks during work'
            ]
        })
    
    return goals
