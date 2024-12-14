document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let currentMonth = date.getMonth();
    let currentYear = date.getFullYear();

    function generateCalendar(month, year) {
        const firstDay = new Date(year, month).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const calendarBody = document.getElementById("calendar-body");
        const monthYear = document.getElementById("month-year");
    
        monthYear.textContent = `${monthNames[month]} ${year}`;
    
        // Clear previous calendar
        calendarBody.innerHTML = '';
    
        let row = document.createElement("tr");
        for (let i = 0; i < firstDay; i++) {
            row.appendChild(document.createElement("td"));
        }
    
        for (let day = 1; day <= daysInMonth; day++) {
            const cell = document.createElement("td");
            if ( day < 10 ) { cell.textContent = "0"+day } else{
                cell.textContent = day
            }
            
            cell.classList.add("calendar-day");
            if ( day < 10 ) { 
                cell.setAttribute('data-day', year + "-" + (currentMonth + 1) + "-" + day.toString().padStart(2, '0')); 
            } else{
                    cell.setAttribute('data-day', year + "-" + (currentMonth + 1) + "-" + day.toString().padStart(2, '0')); 
                }
                
            

            // Mark the current day with a special class
            if (day === date.getDate() && month === date.getMonth() && year === date.getFullYear()) {
                cell.classList.add("current-day");
            }
    
            row.appendChild(cell);
    
            if (row.children.length === 7) {
                calendarBody.appendChild(row);
                row = document.createElement("tr");
            }
        }
    
        if (row.children.length > 0) {
            calendarBody.appendChild(row);
        }
    }

    // Previous Month
    document.getElementById("prev").addEventListener("click", function() {
        if (currentMonth === 0) {
            currentMonth = 11;
            currentYear--;
        } else {
            currentMonth--;
        }
        generateCalendar(currentMonth, currentYear);
    });
    
    // Next Month
    document.getElementById("next").addEventListener("click", function() {
        if (currentMonth === 11) {
            currentMonth = 0;
            currentYear++;
        } else {
            currentMonth++;
        }
        generateCalendar(currentMonth, currentYear);
    });

    // Initial calendar generation
    generateCalendar(currentMonth, currentYear);

    document.querySelectorAll('td').forEach(td => {
        td.addEventListener('click', function(){
            console.log(this.dataset.day)  
            fetch(`calendar_tasks/${this.dataset.day}`)
            .then(response => response.text() )
            .then( data => {
                console.log(data)
                displayModal(data)
            })
            .catch(error => {
                console.log(error)
            })
        })
    })

});
