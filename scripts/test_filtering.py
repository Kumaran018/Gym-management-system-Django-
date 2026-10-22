import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_project.settings')
import django
django.setup()

from django.test import Client
from apps.authentication.models import CustomUser

def test_roles():
    print("Testing personalization across roles...", flush=True)
    c = Client(SERVER_NAME='127.0.0.1')

    # Test kumaran_18
    u_kumaran = CustomUser.objects.get(username='kumaran_18')
    c.force_login(u_kumaran)
    
    r_w = c.get('/workouts/')
    r_d = c.get('/diets/')
    r_p = c.get('/payments/')
    r_m = c.get('/members/')
    
    w_html = r_w.content.decode('utf-8')
    d_html = r_d.content.decode('utf-8')
    p_html = r_p.content.decode('utf-8')
    m_html = r_m.content.decode('utf-8')

    print(f"kumaran_18 - Workouts count: {w_html.count('Workout Plan for')}", flush=True)
    print(f"kumaran_18 - Diets count: {d_html.count('Diet Plan for')}", flush=True)
    print(f"kumaran_18 - Payments count: {p_html.count('INV-2026-')}", flush=True)
    
    assert 'Workout Plan for Kumaran' in w_html, "Kumaran's workout must be in workouts"
    assert 'Workout Plan for Alice' not in w_html, "Other members' workouts must NOT be in Kumaran's workouts"
    assert 'Diet Plan for Kumaran' in d_html, "Kumaran's diet must be in diets"
    assert 'Diet Plan for Alice' not in d_html, "Other members' diets must NOT be in Kumaran's diets"
    assert 'INV-2026-0001' in p_html, "Kumaran's invoice must be in payments"
    assert 'INV-2026-0008' not in p_html, "Alice's invoice must NOT be in Kumaran's payments"
    print("--> Kumaran personalization: 100% VERIFIED!", flush=True)

    # Test member1 (Alice)
    u_alice = CustomUser.objects.get(username='member1')
    c.force_login(u_alice)
    
    r_w_a = c.get('/workouts/')
    r_d_a = c.get('/diets/')
    r_p_a = c.get('/payments/')
    
    w_a_html = r_w_a.content.decode('utf-8')
    d_a_html = r_d_a.content.decode('utf-8')
    p_a_html = r_p_a.content.decode('utf-8')
    
    assert 'Workout Plan for Alice' in w_a_html, "Alice's workout must be in workouts"
    assert 'Workout Plan for Kumaran' not in w_a_html, "Kumaran's workout must NOT be in Alice's workouts"
    assert 'Diet Plan for Alice' in d_a_html, "Alice's diet must be in diets"
    assert 'Diet Plan for Kumaran' not in d_a_html, "Kumaran's diet must NOT be in Alice's diets"
    assert 'INV-2026-0008' in p_a_html, "Alice's invoice must be in payments"
    assert 'INV-2026-0001' not in p_a_html, "Kumaran's invoice must NOT be in Alice's payments"
    print("--> Alice personalization: 100% VERIFIED!", flush=True)

    # Test admin
    u_admin = CustomUser.objects.get(username='admin')
    c.force_login(u_admin)
    r_w_adm = c.get('/workouts/')
    r_d_adm = c.get('/diets/')
    r_p_adm = c.get('/payments/')
    
    w_adm_html = r_w_adm.content.decode('utf-8')
    d_adm_html = r_d_adm.content.decode('utf-8')
    p_adm_html = r_p_adm.content.decode('utf-8')
    
    print(f"admin - Workouts count: {w_adm_html.count('Workout Plan for')}", flush=True)
    print(f"admin - Diets count: {d_adm_html.count('Diet Plan for')}", flush=True)
    print(f"admin - Payments count: {p_adm_html.count('INV-2026-')}", flush=True)
    
    assert w_adm_html.count('Workout Plan for') == 4, "Admin must see all 4 workouts"
    assert d_adm_html.count('Diet Plan for') == 4, "Admin must see all 4 diet plans"
    assert p_adm_html.count('INV-2026-') == 9, "Admin must see all 9 payment invoices"
    print("--> Admin master view: 100% VERIFIED!", flush=True)

if __name__ == '__main__':
    test_roles()
