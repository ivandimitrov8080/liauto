const loadAllJobs = () => {
	for (let i = 0; i < 3600; i += 200) { $(".jobs-search-results-list").animate({ scrollTop: i }); }
}

loadAllJobs()

const getAllJobs = () => {
	return $(".artdeco-entity-lockup__title")
}

const jobs = getAllJobs()
let jobIndex = 0
let isApplying = false;

const notPresent = (selector) => {
	return $(selector).length == 0 || !$(selector).is(":visible")
}

const chooseDefaultResume = () => {
	if (notPresent(".jobs-resume-picker__resume-btn-container"))
		return false
	$(".jobs-resume-picker__resume-btn-container").children("button")[0].click()
	return true
}

const continueToNextStep = () => {
	if (notPresent("[aria-label='Continue to next step']"))
		return false
	$("[aria-label='Continue to next step']").click()
	return true
}

const reviewApplication = () => {
	if (notPresent("[aria-label='Review your application']"))
		return false
	$("[aria-label='Review your application']").click()
	return true
}

const submitApplication = () => {
	if (notPresent("[aria-label='Submit application']"))
		return false
	$("[aria-label='Submit application']").click()
	return true
}

const nextJob = () => {
	jobs[jobIndex++].click()
	isApplying = false
}

const apply = () => {
	if (notPresent(".jobs-apply-button--top-card"))
		return false
	$($(".jobs-apply-button--top-card")[0]).children("button").click()
	isApplying = true
	return true
}

setInterval(() => {
	if (!isApplying) {
		apply()
	}
	chooseDefaultResume()
	continueToNextStep() || reviewApplication() || (submitApplication() && nextJob())
}, 1000)

