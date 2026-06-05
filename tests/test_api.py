import os, requests, uuid
BASE = os.environ.get('REACT_APP_BACKEND_URL', 'https://playbeat-admin.preview.emergentagent.com').rstrip('/')
TOKEN = os.environ.get('TEST_TOKEN')
H = {"Authorization": f"Bearer {TOKEN}"}

def test_auth_me():
    r = requests.get(f"{BASE}/api/auth/me", headers=H)
    assert r.status_code == 200, r.text
    assert r.json().get("email")

def test_auth_unauth():
    r = requests.get(f"{BASE}/api/auth/me")
    assert r.status_code == 401

def test_dashboard_stats():
    r = requests.get(f"{BASE}/api/dashboard/stats", headers=H)
    assert r.status_code == 200, r.text
    d = r.json()
    for k in ["total_revenue","total_customers","total_orders","pending_orders"]:
        assert k in d

def test_customer_crud():
    payload = {"name":"TEST_Cust","email":f"test_{uuid.uuid4().hex[:6]}@ex.com","phone":"123","country":"US"}
    r = requests.post(f"{BASE}/api/customers", json=payload, headers=H)
    assert r.status_code == 200, r.text
    cid = r.json()["customer_id"]
    assert r.json()["email"] == payload["email"]
    # GET
    g = requests.get(f"{BASE}/api/customers/{cid}", headers=H)
    assert g.status_code == 200 and g.json()["name"] == "TEST_Cust"
    # UPDATE
    u = requests.put(f"{BASE}/api/customers/{cid}", json={"name":"TEST_Updated"}, headers=H)
    assert u.status_code == 200 and u.json()["name"] == "TEST_Updated"
    # LIST
    l = requests.get(f"{BASE}/api/customers", headers=H)
    assert l.status_code == 200 and any(c["customer_id"]==cid for c in l.json())
    # DELETE
    d = requests.delete(f"{BASE}/api/customers/{cid}", headers=H)
    assert d.status_code == 200
    nf = requests.get(f"{BASE}/api/customers/{cid}", headers=H)
    assert nf.status_code == 404

def test_product_crud():
    payload = {"name":"TEST_Prod","price":19.99,"category":"software","product_type":"digital_download"}
    r = requests.post(f"{BASE}/api/products", json=payload, headers=H)
    assert r.status_code == 200, r.text
    pid = r.json()["product_id"]
    g = requests.get(f"{BASE}/api/products/{pid}", headers=H)
    assert g.status_code == 200 and g.json()["price"] == 19.99
    u = requests.put(f"{BASE}/api/products/{pid}", json={"price":29.99}, headers=H)
    assert u.status_code == 200 and u.json()["price"] == 29.99
    d = requests.delete(f"{BASE}/api/products/{pid}", headers=H)
    assert d.status_code == 200

def test_orders_list():
    r = requests.get(f"{BASE}/api/orders", headers=H)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_customer_invalid_email():
    r = requests.post(f"{BASE}/api/customers", json={"name":"X","email":"notanemail"}, headers=H)
    assert r.status_code == 422
