SELECT
    Product,
    Quantity,
    [Sales Price],
    Discount,
    Revenue AS RecordedRevenue,

    ([Sales Price] * Quantity) AS GrossSales,

    ([Sales Price] * Quantity - Discount) AS CalculatedRevenue,

    Revenue - ([Sales Price] * Quantity - Discount)
        AS RevenueDifference

FROM SupermarketSales

WHERE ABS(
    Revenue - ([Sales Price] * Quantity - Discount)
) >= 0.01

ORDER BY ABS(
    Revenue - ([Sales Price] * Quantity - Discount)
) DESC;

SELECT TOP 20
    Product,
    Quantity,
    [Sales Price],
    Discount,
    Revenue,
    Profit,
    [COGs],
    ([Sales Price] * Quantity) AS GrossSales,
    ([Sales Price] * Quantity) - Revenue AS DifferenceFromGross
FROM SupermarketSales
ORDER BY Product, Quantity DESC;

SELECT
    COUNT(*) AS TotalRecords,

    SUM(CASE
        WHEN ABS(Profit - (Revenue - COGS)) < 0.01
        THEN 1 ELSE 0
    END) AS MatchingProfitRecords,

    SUM(CASE
        WHEN ABS(Profit - (Revenue - COGS)) >= 0.01
        THEN 1 ELSE 0
    END) AS MismatchedProfitRecords,

    SUM(Profit) AS TotalRecordedProfit,

    SUM(Revenue - COGS) AS CalculatedTotalProfit

FROM SupermarketSales;

SELECT
    COUNT(*) AS TotalRecords,

    SUM(CASE
        WHEN ABS(Revenue - ([Sales Price] * Quantity)) < 0.01
        THEN 1 ELSE 0
    END) AS RevenueMatchesGrossSales,

    SUM(CASE
        WHEN ABS(Revenue - ([Sales Price] * Quantity)) >= 0.01
        THEN 1 ELSE 0
    END) AS RevenueDiffersFromGrossSales,

    SUM(Revenue) AS TotalRevenue,

    SUM([Sales Price] * Quantity) AS TotalGrossSales,

    SUM(Discount) AS TotalDiscount

FROM SupermarketSales;

SELECT
    COUNT(*) AS TotalRecords,

    SUM(CASE
        WHEN ABS(Profit - (Revenue - COGS)) < 0.01
        THEN 1 ELSE 0
    END) AS MatchingProfitRecords,

    SUM(CASE
        WHEN ABS(Profit - (Revenue - COGS)) >= 0.01
        THEN 1 ELSE 0
    END) AS MismatchedProfitRecords,

    SUM(Profit) AS TotalRecordedProfit,

    SUM(Revenue - COGS) AS CalculatedTotalProfit

FROM SupermarketSales;

SELECT
    DB_NAME() AS CurrentDatabase,
    COUNT(*) AS TotalRecords
FROM dbo.SupermarketSales;

SELECT
    COUNT(*) AS TotalRecords,

    SUM(CASE
        WHEN ABS(Profit - (Revenue - COGS)) < 0.01
        THEN 1 ELSE 0
    END) AS MatchingProfitRecords,

    SUM(CASE
        WHEN ABS(Revenue - ([Sales Price] * Quantity)) < 0.01
        THEN 1 ELSE 0
    END) AS RevenueMatchesGrossSales,

    SUM(Revenue) AS TotalRevenue,

    SUM(COGS) AS TotalCOGS,

    SUM(Profit) AS TotalProfit,

    SUM([Sales Price] * Quantity) AS TotalGrossSales,

    SUM(Discount) AS TotalDiscount

FROM dbo.SupermarketSales;

SELECT
    DB_NAME() AS CurrentDatabase,
    OBJECT_ID('dbo.SupermarketSales') AS TableObjectID,
    COUNT(*) AS TotalRecords,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM dbo.SupermarketSales;