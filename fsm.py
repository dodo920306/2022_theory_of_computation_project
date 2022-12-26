from transitions.extensions import GraphMachine

class FSMModel(GraphMachine):
    fsm_filename = "fsm.png"
    state = ""

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.state = 'default'
    def state_about_us(self):
        self.state = 'about'
    def state_location(self):
        self.state = 'location'
    def state_book(self):
        self.state = 'book'
    def state_admin(self):
        self.state = 'admin'
    def state_talk(self):
        self.state = 'talk'
    def state_category(self):
        self.state = 'category'
    def state_service(self):
        self.state = 'service'
    def state_date(self):
        self.state = 'date'
    def state_time(self):
        self.state = 'time'
    def state_confirm(self):
        self.state = 'confirm'
    def state_confirmed(self):
        self.state = 'confirmed'
    def state_notconfirmed(self):
        self.state = 'default'
    def state_cancel(self):
        self.state = 'cancel'
    def state_canceled(self):
        self.state = 'canceled'