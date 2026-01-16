const CSV_URL =
  "https://docs.google.com/spreadsheets/d/1tT9bwV1jCgTx8utL0vvSqZUWqQi1JiWEXaWvhd9G__Y/gviz/tq?tqx=out:csv&gid=0";

const DATE_REGEX = /^\d{1,2}\/\d{1,2}\/\d{4}$/;

const snowClass = (value) => {
  const amount = Number(value) || 0;
  if (amount <= 0) return "snow-0";
  if (amount <= 2) return "snow-1-2";
  if (amount <= 6) return "snow-3-6";
  if (amount <= 10) return "snow-7-10";
  return "snow-10-plus";
};

const formatValue = (value) => {
  const amount = Number(value) || 0;
  return amount % 1 === 0 ? amount.toFixed(0) : amount.toFixed(2);
};

const buildColumns = (dateColumns) => {
  const columns = [
    { title: "Resort", field: "Resort", frozen: true, headerSort: true },
  ];

  dateColumns.forEach((date) => {
    columns.push({
      title: date,
      field: date,
      hozAlign: "center",
      headerSort: true,
      sorter: "number",
      formatter: (cell) => {
        const value = Number(cell.getValue()) || 0;
        const klass = snowClass(value);
        const width = Math.min(value / 10, 1) * 100;
        return `
          <div class="snow-cell">
            <div class="snow-value">${formatValue(value)}</div>
            <div class="snow-bar">
              <div class="snow-bar-fill ${klass}" style="width:${width}%"></div>
            </div>
          </div>
        `;
      },
    });
  });

  columns.push(
    {
      title: "Five-day total",
      field: "Five-day total",
      hozAlign: "center",
      sorter: "number",
    },
    {
      title: "Forecasted snowfall days",
      field: "Forecasted snowfall days",
      hozAlign: "center",
      sorter: "number",
    },
    { title: "Last Updated", field: "Last_Updated", headerSort: false }
  );

  return columns;
};

const parseDate = (value) => {
  const [month, day, year] = value.split("/").map(Number);
  return new Date(year, month - 1, day);
};

const updateLastUpdated = (rows) => {
  const lastUpdated = rows?.[0]?.["Last_Updated"];
  if (lastUpdated) {
    const el = document.getElementById("last-updated");
    if (el) {
      el.textContent = `Last updated: ${lastUpdated}`;
    }
  }
};

const renderTable = (rows) => {
  const dateColumns = Object.keys(rows[0] || {})
    .filter((key) => DATE_REGEX.test(key))
    .sort((a, b) => parseDate(a) - parseDate(b))
    .slice(0, 5);

  const table = new Tabulator("#forecast-table", {
    data: rows,
    layout: "fitColumns",
    height: "70vh",
    columns: buildColumns(dateColumns),
    initialSort: [{ column: "Five-day total", dir: "desc" }],
  });

  return table;
};

const loadForecast = () => {
  Papa.parse(CSV_URL, {
    download: true,
    header: true,
    dynamicTyping: true,
    complete: (results) => {
      const rows = results.data.filter((row) => row.Resort);
      if (!rows.length) return;
      updateLastUpdated(rows);
      renderTable(rows);
    },
    error: (error) => {
      // eslint-disable-next-line no-console
      console.error("Failed to load CSV", error);
    },
  });
};

loadForecast();
