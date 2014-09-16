Selenium.prototype.doSendSMS = function(phone, message) {
    /**
    * Sends a given SMS message to the given phone number using
    * IdeaMart Simulator and waits for the response
    *
    * @param phone the target phone number
    * @param message the message to be sent
    */
 
	selenium.doType('//div[6]/div/div/div/div[2]/div/input', phone);
	selenium.doType('css=textarea.v-textarea', message);
	selenium.doClick('css=span.v-button-caption');
	selenium.doPause(8000);	// wait till response
};

Selenium.prototype.doSetLBSLocation = function(latitude, longitude) {
    /**
    * Changes the LBS location to the given coordinates on the
    * IdeaMart Simulator
    *
    * @param latitude the latitude of new location
    * @param longitude the longitude of new location
    */
 	
 	// goto LBS tab
	selenium.doClick('//div[@id=\'ROOT-2521314\']/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div/div/table/tbody/tr/td[4]/div/div/div');
	selenium.doType('//div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[7]/div/div/div/div[2]/div/input', longitude);
	selenium.doType('//div[9]/div/div/div/div[2]/div/input', latitude);
	selenium.doClick('//td/div/div');	// back to SMS tab
};
