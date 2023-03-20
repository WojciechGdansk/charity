document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    showFirstFiveElements()
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }


        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;
            pagination(page)
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;
            if (this.currentStep === 2) {
                if (getValuesFromForm() === false) {
                    this.currentStep = 1
                    alert("Wybierz kategorię")
                    return;
                }
            }

            if (this.currentStep === 3) {
                if (howManyBagsToDonate() == "") {
                    this.currentStep = 2
                    alert("Podaj liczbę worków")
                    return;
                }
                foundationsDisplay()
            }

            if (this.currentStep === 4) {
                if (toWhichFoundation() == "") {
                    this.currentStep = 3
                    alert("Wybierz fundację")
                    return;
                }
            }

            if (this.currentStep === 5) {
                if (validateDateAndTime()==true) {
                    this.currentStep =4;
                    alert("Nie można wybrać daty z przeszłości lub niekompletna data/godzina")
                    return ;
                }
                if (validatePhoneNumber()==false) {
                    this.currentStep =4;
                    return ;
                }
                if (validateAddressFields()==false) {
                    this.currentStep =4;
                    alert("Nie uzupełniono pełnego adresu")
                    return ;
                }

            }
            //

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;


            summaryInfo()
        }

        /**
         * Submit form
         *
         *
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
            submitForm()
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

const donateCheckboxes = document.querySelectorAll('input[name="taken"]')
donateCheckboxes.forEach((el)=>{
    if (el.checked==true) {
        el.parentElement.parentElement.parentElement.classList = "donated-text-collected"
    }
    el.addEventListener('click', ()=>{
        if (el.checked==true) {
            el.nextElementSibling.innerText = "Oznacz jako nieodebrany"
            el.previousElementSibling.innerText = "TAK"
            changeCollectedInfo(el.value)
            el.parentElement.parentElement.parentElement.classList = "donated-text-collected"

        }
        else if (el.checked == false) {
            el.nextElementSibling.innerText = "Oznacz jako odebrany"
            el.previousElementSibling.innerText = "NIE"
            changeCollectedInfo(el.value)
            el.parentElement.parentElement.parentElement.classList = "donated-text"
        }

    })
})

});

function getValuesFromForm() {
    const categoryArray = []
    const checkboxes = document.querySelectorAll('.form-group--checkbox > label > input[type="checkbox"]')
    checkboxes.forEach(function (el) {
        if (el.checked) {
            categoryArray.push(el.value)
        }
    })
    if (categoryArray.length < 1) {
        return false
    }
    return categoryArray
}

function foundationsDisplay() {
    const selectedCategories = getValuesFromForm()
    const foundations = document.querySelectorAll('.foundations-list')
    foundations.forEach((el) => {
        el.parentElement.parentElement.removeAttribute('style')
        const foundationCategories = el.dataset.category.split(',')
        const isCommonCategory = selectedCategories.some(r => foundationCategories.includes(r))
        if (isCommonCategory === false) {
            el.parentElement.parentElement.style.display = "none"
        }
    })
}

function howManyBagsToDonate() {
    const countBags = document.querySelector('input[name="bags"]').value
    return countBags
}

function toWhichFoundation() {
    let selectedFoundation = ""
    const allFoundations = document.querySelectorAll('input[type="radio"]')
    allFoundations.forEach((el) => {
        if (el.checked) {
            selectedFoundation = el.value
        }
    })
    return selectedFoundation

}


function pickUpAddress() {
    let addressDetails = []
    const address = document.querySelectorAll('.address-section > div > label > input')
    address.forEach((el) => {
        addressDetails.push(el.value)
    })
    return addressDetails
}

function summaryInfo() {
    const giveAwayGoods = document.querySelector('.bags-description')
    const whichFundation = toWhichFoundation()
    giveAwayGoods.innerText = howManyBagsToDonate() + " " + wordDeclination()
    const selectedFoundation = document.querySelector('.foundation-selected-details')
    selectedFoundation.innerText = whichFundation
    const addressField = document.querySelector('.address-summary-to-add')
    const addressDetails = pickUpAddress()
    addDetailsToSummaryFields(addressField, addressDetails)
    const dateTimeField = document.querySelector('.datetime-selected-display')
    addDetailsToSummaryFields(dateTimeField, getDateTimeInfoFromForm())

}

function wordDeclination() {
    let pluralWord = "worek"
    const whenWorki = [5, 6, 7, 8, 9]
    const lastDigitOfBagsString = howManyBagsToDonate().toString().slice(-1)
    const lastDigitofBagsInteger = parseInt(lastDigitOfBagsString)
    if (howManyBagsToDonate() > 5 && howManyBagsToDonate() < 21 || whenWorki.includes(lastDigitofBagsInteger) === true) {
        pluralWord = "worków"
    } else {
        pluralWord = "worki"
    }
    return pluralWord
}

function addDetailsToSummaryFields(selectorToAdd, detailsToAdd) {
    selectorToAdd.innerHTML = ''
    const addressField = document.querySelector('.address-summary-to-add')
    const addressDetails = pickUpAddress()
    for (let i = 0; i < detailsToAdd.length; i++) {
        const li = document.createElement('li')
        li.innerText = detailsToAdd[i]
        selectorToAdd.appendChild(li)
    }
}

function getDateTimeInfoFromForm() {
    let dateTimeSelected = []
    const dateTimeDetails = document.querySelectorAll('.date-time-details-section > div > label > input')
    dateTimeDetails.forEach((el) => {
        dateTimeSelected.push(el.value)
    })
    const addressAdditionalInfo = document.querySelector('textarea[name="more_info"]')
    if (addressAdditionalInfo.value == "") {
        dateTimeSelected.push("Brak uwag")
    } else {
        dateTimeSelected.push(addressAdditionalInfo.value)
    }
    return dateTimeSelected
}

function validateDateAndTime() {
    const date = getDateTimeInfoFromForm()[0]
    const time = getDateTimeInfoFromForm()[1]
    if (date == "" || time == "") {
        return true
    }
    const datetime = new Date(date + " " + time)
    const now = new Date()
    return datetime < now;
}

function submitForm() {
    const form = document.querySelector("form")
    form.submit()
}

function validatePhoneNumber() {
    const phone = document.querySelector('input[type="phone"]')
    if (isNaN(phone.value)) {
        alert("Numer telefonu może zawierać tylko cyfry")
        return false
    }
    if (phone.value.length < 5) {
        alert("Za krótki numer telefonu")
        return false
    }
    return true
}

function validateAddressFields() {
    for (let i=0;i<pickUpAddress().length; i++) {
        if (pickUpAddress()[i].length<1) {
            return false
        }
    }
}




function changeCollectedInfo(donationId) {
    const response = fetch(`/change_if_collected/${donationId}`)
        .then((res)=>{
            if (!res.ok) {
                alert("Błąd")
                location.reload()
            }
        })
}

function pagination(page) {
    const allLiItems = document.querySelectorAll('.li-select')
    const visibleItems = document.querySelectorAll(`.li-select[data-page="${page}"]`)
    allLiItems.forEach((el)=>{
        const isElInVisibleItems = Array.prototype.indexOf.call(visibleItems, el)
        if (isElInVisibleItems !== -1) {
            el.style.display = "flex"
        }
        else {
            el.style.display = "none"
        }
    })

}

function showFirstFiveElements() {
    const noFirstFiveElements = document.querySelectorAll('.li-select:not([data-page="1"])')
    noFirstFiveElements.forEach((el)=>{
        el.style.display = "none"
    })
}