const CSV_URL =
  "https://docs.google.com/spreadsheets/d/1tT9bwV1jCgTx8utL0vvSqZUWqQi1JiWEXaWvhd9G__Y/gviz/tq?tqx=out:csv&gid=0";

const DATE_REGEX = /^\d{1,2}\/\d{1,2}\/\d{4}$/;

const roundToHalf = (value) => Math.round((Number(value) || 0) * 2) / 2;

const formatDateLabel = (value) => {
  const [month, day, year] = value.split("/").map(Number);
  const date = new Date(year, month - 1, day);
  const weekday = date.toLocaleDateString("en-US", { weekday: "short" });
  return {
    weekday,
    monthDay: `${month}/${day}`,
  };
};

const scaledHeight = (value, maxValue) => {
  const amount = roundToHalf(value);
  if (amount <= 0) return 0;
  const scaled = Math.log1p(amount) / Math.log1p(maxValue);
  return Math.min(scaled, 1) * 100;
};

const snowClass = (value) => {
  const amount = roundToHalf(value);
  if (amount <= 0) return "snow-0";
  if (amount <= 2) return "snow-1-2";
  if (amount <= 6) return "snow-3-6";
  if (amount <= 10) return "snow-7-10";
  return "snow-10-plus";
};

const formatValue = (value) => {
  const amount = roundToHalf(value);
  return amount % 1 === 0 ? amount.toFixed(0) : amount.toFixed(1);
};

const buildColumns = (dateColumns) => {
  const columns = [
    {
      title: "Resort",
      field: "Resort",
      frozen: true,
      headerSort: true,
      cssClass: "resort-col",
      width: 135,
      minWidth: 110,
      maxWidth: 170,
    },
  ];

  dateColumns.forEach((date) => {
    const { weekday, monthDay } = formatDateLabel(date);
    columns.push({
      title: `${weekday} ${monthDay}`,
      titleFormatter: () =>
        `<span class="date-header"><span class="date-dow">${weekday}</span><span class="date-md">${monthDay}</span></span>`,
      field: date,
      hozAlign: "center",
      headerHozAlign: "center",
      headerSort: true,
      sorter: "number",
      cssClass: "forecast-day",
      width: 78,
      minWidth: 70,
      formatter: (cell) => {
        const value = roundToHalf(cell.getValue());
        const klass = snowClass(value);
        const height = scaledHeight(value, 10);
        return `
          <div class="snow-cell">
            <div class="snow-value">${formatValue(value)}</div>
            <div class="snow-column">
              <div class="snow-column-fill ${klass}" style="height:${height}%"></div>
            </div>
          </div>
        `;
      },
    });
  });

  columns.push({
    title: "5-day total",
    field: "Five-day total",
    hozAlign: "center",
    headerHozAlign: "center",
    sorter: "number",
    cssClass: "forecast-total",
    width: 96,
    minWidth: 86,
    formatter: (cell) => {
      const value = roundToHalf(cell.getValue());
      const klass = snowClass(value);
      const height = scaledHeight(value, 20);
      return `
        <div class="snow-cell">
          <div class="snow-value">${formatValue(value)}</div>
          <div class="snow-column">
            <div class="snow-column-fill ${klass}" style="height:${height}%"></div>
          </div>
        </div>
      `;
    },
  });

  columns.push({
    title: "Snow days",
    titleFormatter: () =>
      `<span class="date-header"><span class="date-dow">Snow</span><span class="date-md">days</span></span>`,
    field: "Forecasted snowfall days",
    hozAlign: "center",
    headerHozAlign: "center",
    sorter: "number",
    cssClass: "forecast-meta",
    width: 90,
    minWidth: 80,
  });

  return columns;
};

const parseDate = (value) => {
  const [month, day, year] = value.split("/").map(Number);
  return new Date(year, month - 1, day);
};

const formatUpdated = (value) => {
  if (!value) return "—";
  const normalized = value.replace(" ", "T");
  const parsed = new Date(normalized);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
};

const updateLastUpdated = (rows) => {
  const lastUpdated = rows?.[0]?.["Last_Updated"];
  if (lastUpdated) {
    const el = document.getElementById("last-updated");
    if (el) {
      el.textContent = `Last updated: ${formatUpdated(lastUpdated)}`;
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
    layout: "fitDataTable",
    height: "70vh",
    rowHeight: 52,
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
