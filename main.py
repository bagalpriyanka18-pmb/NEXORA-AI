from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

from database import engine, Base
import models
from routers import student

app = FastAPI()

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Static Folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Student Router
app.include_router(
    student.router,
    prefix="/students",
    tags=["Students"]
)


# Home API
@app.get("/")
def home():
    return {
        "project": "NEXORA AI",
        "status": "Working",
        "message": "Welcome to NEXORA AI"
    }


# Website
@app.get("/website", response_class=HTMLResponse)
def website(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )


# # Career Roadmap
@app.post("/roadmap", response_class=HTMLResponse)
def roadmap(request: Request, career: str = Form(...)):

    career = career.strip().lower()

    if career == "ai engineer":
        return templates.TemplateResponse(
            request=request,
            name="ai_engineer.html",
            context={
                "request": request
            }
        )

    elif career == "data scientist":
        return templates.TemplateResponse(
            request=request,
            name="data_scientist.html",
            context={
                "request": request
            }
        )

    elif career == "data analyst":
        return templates.TemplateResponse(
            request=request,
            name="data_analyst.html",
            context={
                "request": request
            }
        )
    
    elif career == "python developer":
        return templates.TemplateResponse(
        request=request,
        name="python_developer.html",
        context={
            "request": request
        }
    )

    elif career == "machine learning engineer":
      return templates.TemplateResponse(
        request=request,
        name="machine_learning_engineer.html",
        context={
            "request": request
        }
    )

    else:
         return templates.TemplateResponse(
            request=request,
            name="roadmap.html",
            context={
                "request": request,
                "career": career,
                "roadmap": "<h2>🚀 Career Coming Soon...</h2>"
            }
        )
    
@app.post("/courses", response_class=HTMLResponse)
def courses(career: str = Form(...)):

    career = career.strip().lower()

    if career == "ai engineer":

         result = """
        <h2>📚 AI Engineer Recommended Courses</h2>

        <ul>
            <li>✅ Python Programming</li>
            <li>✅ SQL Basics</li>
            <li>✅ Machine Learning</li>
            <li>✅ Deep Learning</li>
            <li>✅ Generative AI</li>
            <li>✅ LangChain</li>
            <li>✅ FastAPI</li>
        </ul>
        """

    elif career == "data scientist":

        result = """
        <h2>📚 Data Scientist Recommended Courses</h2>

        <ul>
            <li>✅ Python</li>
            <li>✅ Statistics</li>
            <li>✅ Pandas</li>
            <li>✅ NumPy</li>
            <li>✅ Machine Learning</li>
            <li>✅ Power BI</li>
        </ul>
        """

    elif career == "python developer":

      result = """
        <h2>📚 Python Developer Recommended Courses</h2>

        <ul>
            <li>✅ Python Basics</li>
            <li>✅ OOP</li>
            <li>✅ Flask</li>
            <li>✅ FastAPI</li>
            <li>✅ Git & GitHub</li>
        </ul>
        """

    elif career == "data analyst":

        result = """
        <h2>📚 Data Analyst Recommended Courses</h2>

        <ul>
            <li>✅ Excel</li>
            <li>✅ SQL</li>
            <li>✅ Power BI</li>
            <li>✅ Tableau</li>
            <li>✅ Python</li>
        </ul>
        """

    else:

        result = "<h2>🚀 Courses Coming Soon...</h2>"

    return f"""
    <html>

    <head>
        <title>Courses</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>

    <div class="container">

        {result}

        <br><br>

        <a href="/website">
            <button>⬅ Back</button>
        </a>

    </div>

    </body>

    </html>
    """
    
# Stock Prediction
@app.post("/predict", response_class=HTMLResponse)
def predict(stock: str = Form(...)):

    stock = stock.upper() + ".NS"

    try:
        data = yf.Ticker(stock)
        info = data.history(period="2d")

        if info.empty:
            raise Exception("No data found")

        current_price = round(info["Close"].iloc[-1], 2)
        previous_price = round(info["Close"].iloc[-2], 2)
        change = round(current_price - previous_price, 2 )
        data_30 = yf.Ticker(stock).history(period="30d")



        plt.figure(figsize=(8,4))
        plt.plot(data_30.index, data_30["Close"])
        plt.title(f"{stock.replace('.NS','')} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)

        plt.savefig("static/stock_graph.png")
        plt.close()

        # Prediction
        if change > 0:
            prediction = "📈 Bullish"
            recommendation = "🟢 BUY"
            reason = "Stock price is increasing."
        elif change < 0:
            prediction = "📉 Bearish"
            recommendation = "🔴 SELL"
            reason = "Stock price is decreasing."
        else:
            prediction = "⚖ Stable"
            recommendation = "🟡 HOLD"
            reason = "Stock price is stable."

        return f"""
        <html>

        <head>
            <title>Stock Prediction</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>

        <body>

        <div class="container">

            <h1>📈 Stock Prediction</h1>

            <h2>{stock.replace(".NS","")}</h2>

            <p><b>Current Price:</b> ₹ {current_price}</p>

            <p><b>Previous Close:</b> ₹ {previous_price}</p>

            <p><b>Today's Change:</b> ₹ {change}</p>

            <p><b>Prediction:</b> {prediction}</p>

            <p><b>Recommendation:</b> {recommendation}</p>

            <p><b>Reason:</b> {reason}</p>

            <br><br>

<img src="/static/stock_graph.png" width="700">
            <br>


            <a href="/website">
                <button>⬅ Back</button>
            </a>

        </div>

        </body>

        </html>
        """

    except:

        return """
        <html>

        <head>
            <title>Error</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>

        <body>

        <div class="container">

            <h2>❌ Invalid Stock Symbol</h2>

            <a href="/website">
                <button>⬅ Back</button>
            </a>

        </div>

        </body>

        </html>
        """

