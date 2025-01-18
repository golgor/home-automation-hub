document.addEventListener("DOMContentLoaded", function () {
    const filterDate = document.getElementById("filter-date");
    const filterName = document.getElementById("filter-name");
    const unmanagedTable = document.querySelector("table.styled-table");
    const managedTable = document.querySelector("table.styled-table");

    // Populate filter dropdowns
    populateFilterDropdowns(unmanagedTable, filterDate, filterName);
    populateFilterDropdowns(managedTable, filterDate, filterName);

    // Add event listeners for sorting
    addSortingEventListeners(unmanagedTable);
    addSortingEventListeners(managedTable);

    // Add event listeners for filtering
    filterDate.addEventListener("change", function () {
        filterTable(unmanagedTable, filterDate.value, filterName.value);
        filterTable(managedTable, filterDate.value, filterName.value);
    });

    filterName.addEventListener("change", function () {
        filterTable(unmanagedTable, filterDate.value, filterName.value);
        filterTable(managedTable, filterDate.value, filterName.value);
    });
});

function populateFilterDropdowns(table, filterDate, filterName) {
    const rows = table.querySelectorAll("tbody tr");
    const dates = new Set();
    const names = new Set();

    rows.forEach((row) => {
        const date = row.querySelector("td[data-label='Date']").textContent;
        const name = row.querySelector("td[data-label='Person']").textContent;
        dates.add(date);
        names.add(name);
    });

    dates.forEach((date) => {
        const option = document.createElement("option");
        option.value = date;
        option.textContent = date;
        filterDate.appendChild(option);
    });

    names.forEach((name) => {
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        filterName.appendChild(option);
    });
}

function addSortingEventListeners(table) {
    const headers = table.querySelectorAll("th.sortable");

    headers.forEach((header) => {
        header.addEventListener("click", function () {
            const isAscending = header.classList.contains("asc");
            const column = header.getAttribute("id");
            sortTable(table, column, !isAscending);
            header.classList.toggle("asc", !isAscending);
            header.classList.toggle("desc", isAscending);
        });
    });
}

function sortTable(table, column, isAscending) {
    const rows = Array.from(table.querySelectorAll("tbody tr"));
    const columnIndex = Array.from(table.querySelectorAll("th")).findIndex(
        (th) => th.getAttribute("id") === column
    );

    rows.sort((a, b) => {
        const aText = a.querySelector(`td:nth-child(${columnIndex + 1})`).textContent;
        const bText = b.querySelector(`td:nth-child(${columnIndex + 1})`).textContent;

        return isAscending ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });

    rows.forEach((row) => table.querySelector("tbody").appendChild(row));
}

function filterTable(table, date, name) {
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach((row) => {
        const rowDate = row.querySelector("td[data-label='Date']").textContent;
        const rowName = row.querySelector("td[data-label='Person']").textContent;

        const isDateMatch = !date || rowDate === date;
        const isNameMatch = !name || rowName === name;

        row.style.display = isDateMatch && isNameMatch ? "" : "none";
    });
}
