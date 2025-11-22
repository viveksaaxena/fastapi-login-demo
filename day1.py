from fastapi import FastAPI, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

# Initialize the FastAPI application
app = FastAPI(title="Simple FastAPI Login App")

# --- WARNING: यह कोड असुरक्षित है और केवल प्रदर्शन (Demonstration) के लिए है। ---
# किसी भी वास्तविक एप्लिकेशन में, आपको पासवर्ड को हमेशा हैश (hash) करना चाहिए।

# --- FIREBASE/FIRESTORE SIMULATION (Simplest Form) ---
# यह डिक्शनरी वास्तविक Firestore कलेक्शन का अनुकरण करती है।
# key: username (email), value: plain_text_password (असुरक्षित!)
USERS = {
    "testuser": "testpass",
     "India": "Delhi" ,
     "MP": "Bhopal"# सादा टेक्स्ट पासवर्ड (INSECURE!)
}

# --- HTML Generation Functions (Login and Register Forms) ---

def get_login_form_html(message: str = "") -> str:
    """रिस्पॉन्सिव लॉगिन फॉर्म के लिए HTML सामग्री जेनरेट करता है।"""
    tailwind_script = '<script src="https://cdn.tailwindcss.com"></script>'
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI लॉगिन</title>
        {tailwind_script}
        <style>
            body {{ font-family: 'Inter', sans-serif; }}
        </style>
    </head>
    <body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
        <div class="w-full max-w-sm bg-white p-6 rounded-xl shadow-2xl">
            <h1 class="text-3xl font-extrabold text-gray-800 mb-6 text-center">लॉगिन करें (असुरक्षित डेमो)</h1>
            
            {f'<p class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm font-medium">{message}</p>' if message else ''}
            
            <form action="/login" method="post" class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 mb-1">यूज़रनेम/ईमेल</label>
                    <input 
                        type="text" 
                        name="username" 
                        id="username" 
                        required 
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out"
                        placeholder="अपना यूज़रनेम दर्ज करें"
                    >
                </div>
                
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">पासवर्ड</label>
                    <input 
                        type="password" 
                        name="password" 
                        id="password" 
                        required 
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out"
                        placeholder="अपना पासवर्ड दर्ज करें"
                    >
                </div>
                
                <button 
                    type="submit" 
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
                >
                    लॉगिन
                </button>
            </form>
            
            <div class="mt-6 text-center text-sm text-gray-600">
                <p>क्या आपका अकाउंट नहीं है? 
                    <a href="/register" class="text-indigo-600 hover:text-indigo-800 font-medium">यहाँ रजिस्टर करें</a>
                </p>
                <div class="mt-4 p-3 bg-red-100 rounded-lg border border-red-400">
                    <p class="text-red-700 font-bold">This site build BY VIVEK S to build site contact vivek2399@outlook.com <br> सुरक्षा चेतावनी: यह डेमो पासवर्ड सीधे स्टोर करता है!</p>
                    <p>टेस्ट यूज़र:</p>
                    <p class="font-bold">यूज़रनेम: testuser</p>
                    <p class="font-bold">पासवर्ड: testpass</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def get_register_form_html(message: str = "") -> str:
    """रिस्पॉन्सिव रजिस्ट्रेशन फॉर्म के लिए HTML सामग्री जेनरेट करता है।"""
    tailwind_script = '<script src="https://cdn.tailwindcss.com"></script>'
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI रजिस्ट्रेशन</title>
        {tailwind_script}
        <style>
            body {{ font-family: 'Inter', sans-serif; }}
        </style>
    </head>
    <body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
        <div class="w-full max-w-sm bg-white p-6 rounded-xl shadow-2xl">
            <h1 class="text-3xl font-extrabold text-gray-800 mb-6 text-center">रजिस्टर करें</h1>
            
            {f'<p class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm font-medium">{message}</p>' if message else ''}
            
            <form action="/register" method="post" class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 mb-1">नया यूज़रनेम/ईमेल</label>
                    <input 
                        type="text" 
                        name="username" 
                        id="username" 
                        required 
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out"
                        placeholder="नया यूज़रनेम दर्ज करें"
                    >
                </div>
                
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">पासवर्ड</label>
                    <input 
                        type="password" 
                        name="password" 
                        id="password" 
                        required 
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out"
                        placeholder="एक मजबूत पासवर्ड चुनें"
                    >
                </div>
                
                <button 
                    type="submit" 
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-md text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition duration-150 ease-in-out"
                >
                    अकाउंट बनाएँ
                </button>
            </form>
            
            <div class="mt-6 text-center text-sm text-gray-600">
                <p>पहले से ही अकाउंट है? 
                    <a href="/" class="text-indigo-600 hover:text-indigo-800 font-medium">यहाँ लॉगिन करें</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- FastAPI Routes ---

@app.get("/", response_class=HTMLResponse)
async def login_page():
    """लॉगिन फॉर्म प्रदर्शित करने के लिए रूट। (मुख्य URL)"""
    return get_login_form_html()

@app.get("/login", response_class=RedirectResponse)
async def login_redirect():
    """
    /login पर किसी भी GET रिक्वेस्ट को मुख्य लॉगिन फॉर्म (/) पर रीडायरेक्ट करता है।
    """
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.post("/login", response_class=HTMLResponse)
async def handle_login(username: str = Form(...), password: str = Form(...)):
    """फॉर्म सबमिशन को संभालने और लॉगिन सत्यापन करने के लिए रूट।"""
    
    # --- FIREBASE/FIRESTORE SIMULATION: Read user data by username ---
    stored_password = USERS.get(username)
    
    # Check if the username exists AND the password matches the stored plain text password
    if stored_password and password == stored_password:
        # सफल लॉगिन: /dashboard पर रीडायरेक्ट करें
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        return response
    else:
        # असफल लॉगिन: त्रुटि संदेश के साथ फॉर्म को फिर से प्रदर्शित करें
        error_message = "अमान्य यूज़रनेम या पासवर्ड। कृपया पुनः प्रयास करें।"
        return get_login_form_html(message=error_message)

@app.get("/register", response_class=HTMLResponse)
async def register_page():
    """रजिस्ट्रेशन फॉर्म प्रदर्शित करने के लिए रूट।"""
    return get_register_form_html()

@app.post("/register", response_class=HTMLResponse)
async def handle_registration(username: str = Form(...), password: str = Form(...)):
    """रजिस्ट्रेशन फॉर्म सबमिशन को संभालता है।"""

    if username in USERS:
        error_message = f"यूज़रनेम '{username}' पहले से मौजूद है। कृपया दूसरा चुनें।"
        return get_register_form_html(message=error_message)
    
    # --- WARNING: Storing plain text password (INSECURE) ---
    USERS[username] = password
    
    # सफल रजिस्ट्रेशन: उपयोगकर्ता को लॉगिन पेज पर रीडायरेक्ट करें
    success_response_html = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>रजिस्ट्रेशन सफल</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-green-50 min-h-screen flex flex-col items-center justify-center p-4">
        <div class="bg-white p-8 rounded-xl shadow-2xl text-center">
            <h1 class="text-3xl font-extrabold text-green-600 mb-4">रजिस्ट्रेशन सफल!</h1>
            <p class="text-lg text-gray-700 mb-6">आपका अकाउंट बन गया है। अब आप लॉगिन कर सकते हैं।</p>
            <a href="/" class="inline-block py-2 px-6 border border-transparent rounded-lg shadow-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition duration-150 ease-in-out">
                लॉगिन पर जाएँ
            </a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=success_response_html)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    """सफल लॉगिन के बाद साधारण सफलता पेज।"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>डैशबोर्ड</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-indigo-50 min-h-screen flex flex-col items-center justify-center p-4">
        <div class="bg-white p-8 rounded-xl shadow-2xl text-center">
            <h1 class="text-4xl font-extrabold text-indigo-600 mb-4">सफलतापूर्वक लॉगिन!</h1>
            <p class="text-xl text-gray-700 mb-6">यह आपका सुरक्षित डैशबोर्ड पेज है।</p>
            <a href="/" class="inline-block py-2 px-6 border border-transparent rounded-lg shadow-md text-sm font-medium text-white bg-gray-500 hover:bg-gray-600 transition duration-150 ease-in-out">
                लॉगआउट (वापस लॉगिन पर जाएँ)
            </a>
        </div>
    </body>
    </html>
    """
    return html_content
