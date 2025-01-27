import datetime
import random
from faker            import Faker
from tzlocal          import get_localzone
from .weighted_choice import WeightedChoice


class FakeTokens:
	"""List of methods to generate fake tokens."""

	def __init__(self, faker=None, date=None, date_pattern="%d/%b/%Y:%H:%M:%S", sleep=None):
		self.faker = Faker() if faker is None else faker
		self.otime = datetime.datetime.now() if date is None else datetime.datetime.strptime(date, date_pattern)
		self.dispatcher = {}
		self.date_pattern = date_pattern
		self.sleep = sleep

		self.register_token("b", self.init_size_object())
		self.register_token("d", self.init_date())
		self.register_token("h", self.init_host())
		self.register_token("m", self.init_method())
		self.register_token("s", self.init_status_code())
		self.register_token("u", self.init_user_agent())
		self.register_token("v", self.init_server_name())
		self.register_token("H", self.init_protocol())
		self.register_token("R", self.init_referrer())
		self.register_token("U", self.init_url_request())
		self.register_token("Z", self.init_timezone())
		self.register_token("a", self.init_server_action())
		self.register_token("n", self.init_username())
		self.register_token("t", self.init_time_taken())
		self.register_token("c", self.init_client())
		self.register_token("x", self.init_exception_id())
		self.register_token("C", self.init_content_type())
		self.register_token("S", self.init_uri_scheme())
		self.register_token("P", self.init_uri_port())
		
	def register_token(self, key, method):
		self.dispatcher.update({ key: method })

	def get_tokens(self, date_pattern=None):
		if date_pattern is not None:
			self.date_pattern = date_pattern
		return self.dispatcher

	def run_token(self, token):
		return self.dispatcher[token]()

	def inc_date(self):
		sleep = self.sleep if self.sleep is not None else random.randint(30, 300)
		increment = datetime.timedelta(seconds=sleep)
		self.otime += increment
		return self.otime


	# ----------------------------------------------

	def init_date(self):
		"""Return the date (%d)."""
		def get_date():
			date = self.inc_date()
			return date.strftime(self.date_pattern)

		return get_date

	def init_host(self):
		"""Return the client IP address (%h)."""
		return self.faker.ipv4

	def init_method(self):
		"""Return the request method (%m)."""
		rng = WeightedChoice(["GET", "POST", "DELETE", "PUT"], [0.8, 0.1, 0.05, 0.05])
		return rng.run

	def init_protocol(self):
		"""Return the request protocol (%H)."""
		return lambda: "HTTP/1.0"

	def init_referrer(self):
		"""Return the referrer HTTP request header (%R)."""
		return self.faker.uri

	def init_server_name(self, servers=None):
		"""Return the server name (%v)."""
		if servers is None:
			servers = ["example1", "example2"]
		return lambda: random.choice(servers)

	def init_size_object(self):
		"""Return the size of the object returning by the client (%b)."""
		return lambda: int(random.gauss(5000, 50))

	def init_status_code(self):
		"""Return the HTTP status code (%s)."""
		rng = WeightedChoice(["200", "404", "500", "301"], [0.9, 0.04, 0.02, 0.04])
		return rng.run

	def init_timezone(self):
		"""Return the timezone (%Z)."""
		timezone = datetime.datetime.now(get_localzone()).strftime("%z")
		return lambda: timezone

	def init_url_request(self, list_files=None):
		"""Return the URL path requested (%U)."""
		if list_files is None:
			list_files = []
			for _ in range(0, 10):
				list_files.append(self.faker.file_path(depth=random.randint(0, 2), category="text"))

		return lambda: random.choice(list_files)

	def init_user_agent(self):
		"""Return the user-agent HTTP request header (%u)."""
		user_agent = [self.faker.chrome(), self.faker.firefox(), self.faker.safari(), self.faker.internet_explorer(), self.faker.opera()]
		rng = WeightedChoice(user_agent, [0.5, 0.3, 0.1, 0.05, 0.05])
		return rng.run

	def init_server_action(self):
		"""Return the server actionn (%a)."""
		rng = WeightedChoice(["TCP_DENIED", "TCP_TUNNELED", "TCP_HIT", "TCP_MISS", "TCP_NC_MISS"], [0.9, 0.6, 0.1, 0.05, 0.04])
		return rng.run
		
	def init_username(self):
		"""Return the username (%n). """
		rng = WeightedChoice(["-", "UserNameA", "UserNameB", "UserNameC", "UserNameD"], [0.5, 0.1, 0.1, 0.1, 0.1])
		return rng.run
		
	def init_time_taken(self):
		"""Return the time taken (%t). """
		return lambda: int(random.randint(1, 65535))

	def init_client(self):
		"""Return the client ip (%c). """
		return self.faker.ipv4

	def init_exception_id(self):
		"""Return the Exception ID (%x). """
		rng = WeightedChoice(["authentication_failed", "-", "policy_denied", "policy_redirect"], [0.9, 0.9, 0.1, 0.1])
		return rng.run
		
	def init_content_type(self): 
		"""Return the Content Type (%C). """
		rng = WeightedChoice(["-", "text/xml", "application/javascript", "image/gif", "image/png"], [0.8, 0.1, 0.1, 0.1, 0.1])
		return rng.run
		
	def init_uri_scheme(self):
		"""Return the URI Scheme (%S). """
		rng = WeightedChoice(["tcp", "http", "https"], [0.8, 0.4, 0.1])
		return rng.run
		
	def init_uri_port(self):
		"""Retrn the URI Port (%P)."""
		rng = WeightedChoice(["443", "80", "8088", "81"], [0.8, 0.3, 0.1, 0.1])
		return rng.run
	# ----------------------------------------------
