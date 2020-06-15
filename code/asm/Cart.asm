asm Cart

import ./STDL/StandardLibrary

signature:
	// DOMAINS
	abstract domain Drug
	enum domain States = {WAITING | ADD_PRODUCT_OR_EXIT | CHOOSE_GEN_COM | SELECTED_GENERIC | SELECTED_COMMERCIAL | CLOSED}
	enum domain Actions = {ORDER | EXIT}
	enum domain AddProduct = {YES | NO}
	enum domain Type = {GENERIC | COMMERCIAL}

	// CONTROLLED VARAIBLES
	dynamic controlled cartState: States
	dynamic controlled currentDrug: Drug	
	dynamic controlled outMess: Any	// Output message
	dynamic controlled total: Integer
	dynamic controlled numOfProductsInCart: Integer

	// MONITORED VARAIBLES
	dynamic monitored action: Actions 
	dynamic monitored selectedDrug: Drug 
	dynamic monitored selectedAddProduct: AddProduct
	dynamic monitored selectedDrugType: Type
	dynamic monitored insertQuantity: Integer
	dynamic monitored insertPrice: Integer
	
	// STATIC VARIABLES
	static litio: Drug
	static morfina: Drug
	static paracetamolo: Drug
	
	// DERIVED FUNCTION
	derived valid: Boolean

	// STATIC FUNCTION (N-ARIE)
	static getPrice: Drug -> Integer  
	
definitions:
	// DERIVED FUNCTION
	function valid = numOfProductsInCart < 2 // Max number of products in cart
	
	// STATIC FUNCTION (N-ARIE)
	function getPrice($c in Drug) = // $c Input a string
		switch($c)
			case litio : 7
			case morfina : 10
			case paracetamolo : 4
		endswitch

	// MACRO RULE SUPPORT
	macro rule r_AddGenericToTotal =
		par
		total := total + getPrice(currentDrug)*insertQuantity
		outMess := "Total price updated"
		numOfProductsInCart := numOfProductsInCart + 1
		cartState := ADD_PRODUCT_OR_EXIT
		endpar
	
	macro rule r_AddCommercialToTotal =
		par
		total := total + insertPrice*insertQuantity
		outMess := "Total price updated"
		numOfProductsInCart := numOfProductsInCart + 1
		cartState := ADD_PRODUCT_OR_EXIT
		endpar
	
	// MACRO RULE MAIN
	macro rule r_Waiting =
		if (cartState=WAITING) then
			par
			if (action=ORDER) then
				par
				cartState := ADD_PRODUCT_OR_EXIT
				outMess := "Select a generic or commercial drug"
				endpar
			endif
			
			if (action=EXIT) then
				par
				cartState := CLOSED
				outMess := "Successful!"
				endpar
			endif
			endpar
		endif
	
	macro rule r_SelectAddProductOrExit =
		if (cartState=ADD_PRODUCT_OR_EXIT) then
			par
			if (selectedAddProduct=YES) then
				par
				cartState := CHOOSE_GEN_COM
				outMess := "Choose the type of drugs (generic or commercial)"
				endpar
			endif
			
			if (selectedAddProduct=NO) then
				par
				cartState := WAITING
				outMess := "Order or Exit"
				endpar
			endif
			endpar
		endif

	macro rule r_SelectDrugType =
		if (cartState=CHOOSE_GEN_COM) then
			par
			if (selectedDrugType=GENERIC) then
				par 
				cartState := SELECTED_GENERIC
				outMess := "Insert a name of a generic drug in the list"
				endpar
			endif
			
			if (selectedDrugType=COMMERCIAL) then
				par 
				cartState := SELECTED_COMMERCIAL
				outMess := "Insert a name of a new commercial drug"
				endpar
			endif
			endpar
		endif
	
	macro rule r_DrugDetail =
		par
		if (cartState=SELECTED_GENERIC) then
			if (exist $c in Drug with $c=selectedDrug) then	
				seq // Necessarily sequential
				currentDrug := selectedDrug
				r_AddGenericToTotal[]
				endseq
			endif
		endif
	
		if (cartState=SELECTED_COMMERCIAL) then
			r_AddCommercialToTotal[]
		endif
		endpar
		
	macro rule r_Closing = 
		cartState := CLOSED

	// MAIN RULE
	main rule r_Main =
			if (valid) then
				par
				r_Waiting[]
				r_SelectAddProductOrExit[]
				r_SelectDrugType[]
				r_DrugDetail[]
				endpar
			else
				r_Closing[]
			endif

// INITIAL STATE
default init s0:
	function cartState = WAITING
	function numOfProductsInCart = 0 
	function total = 0 
