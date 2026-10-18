USE SupermarketAI;

SELECT DB_NAME() AS CurrentDatabase;


SELECT
    @@SERVERNAME AS ServerName,
    SERVERPROPERTY('InstanceName') AS InstanceName;

    SELECT
    COUNT(*) AS TotalRecords  
    FROM dbo.SupermarketSales;  

    SELECT
    COLUMN_NAME
    DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'SupermarketSales'

    SELECT TOP 10 * 
    FROM dbo.SupermarketSales   

    SELECT 
    SUM([Revenue]) AS TotalRevenue, 
    SUM([Profit]) AS TotalProfit,   
    SUM([COGS]) AS TotalCOGS,   
    SUM([Quantity]) AS TotalQuantity,   
    SUM([Discount]) AS TotalDiscount 
    FROM SupermarketSales

    SELECT
    AVG(Revenue) AS AverageRevenue,
    AVG(Profit) AS AverageProfit,
    AVG(Discount) AS AverageDiscount
FROM SupermarketSales;

SELECT 
Product,
SUM(Revenue) AS TotalRevenue,
SUM(Profit) AS TotalProfit
FROM SupermarketSales
GROUP BY Product
ORDER BY TotalRevenue DESC;

SELECT
Product,
SUM(QUANTITY) AS TotalQuantity
FROM SupermarketSales
GROUP BY Product    
ORDER BY TotalQuantity DESC;

SELECT
Product,
SUM(Profit) AS TotalProfit  
FROM SupermarketSales
GROUP BY Product
ORDER BY TotalProfit DESC;

SELECT
    [Product Category],
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    SUM(Quantity) AS TotalQuantity
FROM SupermarketSales
GROUP BY [Product Category]
ORDER BY TotalRevenue DESC;

SELECT TOP 10 *
FROM SupermarketSales

SELECT 
City,
SUM(REVENUE) AS TotalRevenue
FROM SupermarketSales
GROUP BY City
ORDER BY TotalRevenue DESC;

SELECT
    City,
    SUM(Profit) AS TotalProfit
FROM SupermarketSales
GROUP BY City
ORDER BY TotalProfit DESC;


SELECT
    [Customer Type],
    SUM(Revenue) AS TotalRevenue
FROM SupermarketSales
GROUP BY [Customer Type]
ORDER BY TotalRevenue DESC;


SELECT
    [Customer Type],
    COUNT(*) AS TotalTransactions,
    SUM(Revenue) AS TotalRevenue,
    AVG(Revenue) AS AverageRevenue
FROM SupermarketSales
GROUP BY [Customer Type]
ORDER BY AverageRevenue DESC;

SELECT
    YEAR([Date]) AS SalesYear,
    MONTH([Date]) AS SalesMonth,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    COUNT(*) AS TotalTransactions
FROM SupermarketSales
GROUP BY
    YEAR([Date]),
    MONTH([Date])
ORDER BY
    SalesYear,
    SalesMonth;

    SELECT
    [Payment Method],
    COUNT(*) AS TotalTransactions,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    AVG(Revenue) AS AverageRevenue
FROM SupermarketSales
GROUP BY [Payment Method]
ORDER BY TotalRevenue DESC;

SELECT 
   [Gender],
    COUNT(*) AS TotalTransactions,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    AVG(Revenue) AS AverageRevenue
    FROM SupermarketSales
    GROUP BY [Gender]
    ORDER BY TotalRevenue DESC; 

    SELECT
        [Country],  
        COUNT(*) AS TotalTransactions,
         SUM(Revenue) AS TotalRevenue,
        SUM(Profit) AS TotalProfit,
        AVG(Revenue) AS AverageRevenue
        FROM SupermarketSales
        GROUP BY [Country]
        ORDER BY TotalRevenue DESC;

    SELECT
    YEAR([Date]) AS SalesYear,
    MONTH([Date]) AS SalesMonth,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM SupermarketSales
GROUP BY
    YEAR([Date]),
    MONTH([Date])
ORDER BY TotalProfit DESC;

/*Which product category has the highest profit margin?
To determine which product category has the highest profit margin, we can calculate the profit margin for each product category using the formula:
Profit Margin = (Total Profit / Total Revenue) * 100*/
 SELECT
    [Product Category],
    SUM(Profit) AS TotalProfit,
    SUM(Revenue) AS TotalRevenue,
    (SUM(Profit) / SUM(Revenue)) * 100.0 AS ProfitMargin
    FROM SupermarketSales
    GROUP BY [Product Category]
    ORDER BY ProfitMargin DESC;

    SELECT
    Product,
    SUM(Quantity) AS TotalQuantity,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    (SUM(Profit) / SUM(Revenue)) * 100.0 AS ProfitMargin
    FROM SupermarketSales
    GROUP BY Product
    ORDER BY ProfitMargin DESC;

    SELECT
    COUNT(*) AS TotalRecords,
    COUNT(Discount) AS NonNullDiscounts,
    MIN(Discount) AS MinimumDiscount,
    MAX(Discount) AS MaximumDiscount,
    AVG(Discount) AS AverageDiscount,
    COUNT(DISTINCT Discount) AS UniqueDiscountValues
FROM SupermarketSales;

SELECT
    AVG(
        (Discount / NULLIF([Sales Price] * Quantity, 0)) * 100
    ) AS AverageDiscountPercentage
FROM SupermarketSales;

SELECT TOP 10
    Product,
    Quantity,
    [Sales Price],
    Discount,
    ([Sales Price] * Quantity) AS GrossSales,
    Revenue AS RecordedRevenue,
    ([Sales Price] * Quantity) - Discount AS CalculatedRevenue
FROM SupermarketSales;

SELECT
    COUNT(*) AS TotalRecords,

    SUM(
        CASE
            WHEN ABS(
                Revenue - ([Sales Price] * Quantity - Discount)
            ) < 0.01
            THEN 1
            ELSE 0
        END
    ) AS MatchingRecords,

    SUM(
        CASE
            WHEN ABS(
                Revenue - ([Sales Price] * Quantity - Discount)
            ) >= 0.01
            THEN 1
            ELSE 0
        END
    ) AS MismatchedRecords,

    SUM(
        Revenue - ([Sales Price] * Quantity - Discount)
    ) AS TotalRevenueDifference

FROM SupermarketSales;