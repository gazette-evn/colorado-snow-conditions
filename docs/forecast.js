const CSV_URL =
  "https://docs.google.com/spreadsheets/d/1tT9bwV1jCgTx8utL0vvSqZUWqQi1JiWEXaWvhd9G__Y/gviz/tq?tqx=out:csv&gid=0";

const DATE_REGEX = /^\d{1,2}\/\d{1,2}\/\d{4}$/;

let currentData = [];
let currentSort = { column: null, dir: "desc" };

const roundToHalf = (value) => Math.round((Number(value) || 0) * 2) / 2;

const formatValue = (value) => {
  const amount = roundToHalf(value);
  return amount % 1 === 0 ? amount.toFixed(0) : amount.toFixed(1);
};

const snowClass = (value) => {
  const amount = roundToHalf(value);
  if (amount <= 0) return "snow-0";
  if (amount <= 2) return "snow-1-2";
  if (amount <= 6) return "snow-3-6";
  if (amount <= 10) return "snow-7-10";
  return "snow-10-plus";
};

const scaledHeight = (value, maxValue = 10) => {
  const amount = roundToHalf(value);
  if (amount <= 0) return 0;
  const scaled = Math.log1p(amount) / Math.log1p(maxValue);
  return Math.min(scaled, 1) * 100;
};

const formatDateHeader = (dateStr) => {
  const [month, day, year] = dateStr.split("/").map(Number);
  const date = new Date(year, month - 1, day);
  const weekday = date.toLocaleDateString("en-US", { weekday: "short" });
  return { weekday, monthDay: `${month}/${day}` };
};

const formatUpdated = (value) => {
  if (!value) return "—";
  const parsed = new Date(value.replace(" ", "T"));
  if (isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
};

const renderDayCell = (value) => {
  const amount = roundToHalf(value);
  const klass = snowClass(amount);
  const height = scaledHeight(amount);
  return `
    <div class="day-cell">
      <div class="day-value">${formatValue(amount)}"</div>
      <div class="day-bar">
        <div class="day-bar-fill ${klass}" style="height:${height}%"></div>
      </div>
    </div>
  `;
};

const sortData = (data, column, dir) => {
  return [...data].sort((a, b) => {
    const aVal = column === "Resort" ? a[column] : Number(a[column]) || 0;
    const bVal = column === "Resort" ? b[column] : Number(b[column]) || 0;
    
    if (column === "Resort") {
      return dir === "asc" ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
    return dir === "asc" ? aVal - bVal : bVal - aVal;
  });
};

const renderTable = (data, dateColumns) => {
  const headerRow = document.getElementById("header-row");
  const tbody = document.getElementById("table-body");
  
  // Render headers
  let headers = `<th data-column="Resort">Resort</th>`;
  dateColumns.forEach((col) => {
    const { weekday, monthDay } = formatDateHeader(col);
    headers += `<th data-column="${col}">${weekday}<br>${monthDay}</th>`;
  });
  headerRow.innerHTML = headers;
  
  // Render rows
  tbody.innerHTML = data
    .map((row) => {
      let cells = `<td>${row.Resort}</td>`;
      dateColumns.forEach((col) => {
        cells += `<td>${renderDayCell(row[col])}</td>`;
      });
      return `<tr>${cells}</tr>`;
    })
    .join("");
  
  // Update sort indicators
  document.querySelectorAll("th").forEach((th) => {
    th.classList.remove("sorted-asc", "sorted-desc");
    if (th.dataset.column === currentSort.column) {
      th.classList.add(`sorted-${currentSort.dir}`);
    }
  });
};

const handleSort = (column) => {
  if (currentSort.column === column) {
    currentSort.dir = currentSort.dir === "asc" ? "desc" : "asc";
  } else {
    currentSort.column = column;
    currentSort.dir = "desc";
  }
  
  const dateColumns = Object.keys(currentData[0] || {})
    .filter((key) => DATE_REGEX.test(key))
    .sort()
    .slice(0, 5);
  
  const sorted = sortData(currentData, column, currentSort.dir);
  renderTable(sorted, dateColumns);
};

const loadForecast = () => {
  Papa.parse(CSV_URL, {
    download: true,
    header: true,
    dynamicTyping: true,
    complete: (results) => {
      const rows = results.data
        .filter((row) => row.Resort && row.Resort.trim())
        .map((row) => {
          const cleaned = {};
          Object.keys(row).forEach((key) => {
            if (key && key.trim()) {
              cleaned[key] = row[key];
            }
          });
          return cleaned;
        });
      
      if (!rows.length) return;
      
      currentData = rows;
      
      // Update timestamp
      const lastUpdated = rows[0]?.["Last_Updated"];
      if (lastUpdated) {
        document.getElementById("last-updated").textContent = `Updated: ${formatUpdated(lastUpdated)}`;
      }
      
      // Get date columns
      const dateColumns = Object.keys(rows[0])
        .filter((key) => DATE_REGEX.test(key))
        .sort()
        .slice(0, 5);
      
      // Initial render (sorted descending by first date column)
      currentSort.column = dateColumns[dateColumns.length - 1];
      const sorted = sortData(rows, currentSort.column, "desc");
      renderTable(sorted, dateColumns);
      
      // Add click handlers
      document.querySelectorAll("th[data-column]").forEach((th) => {
        th.addEventListener("click", () => handleSort(th.dataset.column));
      });
    },
    error: (error) => {
      console.error("Failed to load CSV", error);
    },
  });
};

loadForecast();
