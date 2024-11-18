import base64
import io
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, url_for, request, flash, redirect
from app.db_connect import get_db
import pandas as pd
from app.functions import total_sales_by_region, monthly_sales_trend, top_performing_region


sales = Blueprint('sales', __name__)

@sales.route('/show_sales')
def show_sales():
    connection = get_db()

    query = "SELECT * FROM sales_data"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    df = pd.DataFrame(result)

    df['Actions'] = df['sales_data_id'].apply(lambda id:
        f'<a href="{url_for("sales.edit_sales_data", sales_data_id=id)}" class="btn btn-sm btn-info">Edit</a> '
        f'<form action="{url_for("sales.delete_sales_data", sales_data_id=id)}" method="post" style="display:inline;">'           
        f'<button type="submit" class ="btn btn-sm btn-danger">Delete</button></form>'
    )

    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, header=False,
                            escape=False)
    rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

    return render_template("sales_data.html", table=rows_only)

@sales.route('/add_sales_data', methods=['GET', 'POST'])
def add_sales_data():
    if request.method == 'POST':
        # Check if 'region' exists in the form data
        if 'region' not in request.form:
            flash("Region field is missing in the form submission.", "danger")
            return redirect(url_for('sales.add_sales_data'))

        # Proceed if 'region' is present
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region = request.form['region']

        connection = get_db()
        query = "INSERT INTO sales_data (monthly_amount, date, region) VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (monthly_amount, date, region))
        connection.commit()
        flash("New sales data added successfully!", "success")

        return redirect(url_for('sales.show_sales'))

    return render_template("add_sales_data.html")



@sales.route('/edit_sales_data/<int:sales_data_id>', methods=['GET', 'POST'])
def edit_sales_data(sales_data_id):
    connection = get_db()
    if request.method == 'POST':
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region = request.form['region']

        query = "UPDATE sales_data SET monthly_amount = %s, date = %s, region = %s WHERE sales_data_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (monthly_amount, date, region, sales_data_id))
        connection.commit()
        flash("Sales data updated successfully", "success")
        return redirect(url_for('sales.show_sales'))

    query = "SELECT * FROM sales_data WHERE sales_data_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (sales_data_id,))
        sales_data = cursor.fetchone()  # fetchone() returns a single record as a dictionary

    return render_template("edit_sales_data.html", sales_data=sales_data)


@sales.route('/delete_sales_data/<int:sales_data_id>', methods=['POST'])
def delete_sales_data(sales_data_id):
    connection = get_db()

    query = "DELETE FROM sales_data WHERE sales_data_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (sales_data_id,))
    connection.commit()
    flash("Sales data deleted successfully", "success")
    return redirect(url_for('sales.show_sales'))


@sales.route('/reports')
def reports():
    connection = get_db()

    # Fetch all sales data
    query = "SELECT * FROM sales_data"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    # Convert to DataFrame for analysis
    df = pd.DataFrame(result)

    # Generate analysis results
    sales_by_region = total_sales_by_region(df)
    monthly_trend = monthly_sales_trend(df)
    top_region = top_performing_region(df)

    # Convert results to HTML tables
    sales_by_region_html = sales_by_region.to_html(classes='table table-striped table-bordered', index=False)
    monthly_trend_html = monthly_trend.to_html(classes='table table-striped table-bordered', index=False)
    top_region_html = top_region.to_html(classes='table table-striped table-bordered', index=False)

    # Pass HTML tables to the template
    return render_template("reports.html", sales_by_region=sales_by_region_html,
                           monthly_trend=monthly_trend_html, top_region=top_region_html)


@sales.route('/visualization')
def visualization():
    connection = get_db()

    # Fetch data from the database
    query = "SELECT region, SUM(monthly_amount) AS total_sales FROM sales_data GROUP BY region"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    # Convert result to DataFrame
    df = pd.DataFrame(result)
    df['region'] = df['region'].astype(int)  # Ensure region is an integer

    # Generate a bar chart
    fig, ax = plt.subplots()
    ax.bar(df['region'], df['total_sales'], color='skyblue')
    ax.set_xlabel('Region')
    ax.set_ylabel('Total Sales')
    ax.set_title('Total Sales by Region')

    # Ensure x-axis or y-axis has whole numbers only
    ax.get_xaxis().get_major_locator().set_params(integer=True)
    ax.get_yaxis().get_major_locator().set_params(integer=True)

    # Convert plot to PNG image
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template("visualization.html", chart_url=chart_url)