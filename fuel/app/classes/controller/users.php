<?php
/**
 * Materia
 * License outlined in licenses folder
 */

class Controller_Users extends Controller
{
	public function before()
	{
		$this->theme = Theme::instance();
		$this->theme->set_template('layouts/main');

		Css::push_group("core");
		Js::push_group("core");
		Js::push_group("student");
	}

	public function after($response)
	{
		// If no response object was returned by the action,
		if (empty($response) or ! $response instanceof Response)
		{
			// render the defined template
			$me = Model_User::find_current();
			if ($me)
			{
				// add beardmode
				if ( ! empty($me->profile_fields['beardMode']))
				{
					Js::push_inline('var BEARD_MODE = true;');
				}
			}
			$this->theme->set_partial('header', 'partials/header')->set('me', $me);

			// add google analytics
			if ($gid = Config::get('materia.google_tracking_id', false))
			{
				Js::push_inline($this->theme->view('partials/google_analytics', array('id' => $gid)));
			}

			Js::push_inline('var BASE_URL = "'.Uri::base().'";');
			Js::push_inline('var WIDGET_URL = "'.Config::get('materia.urls.engines').'";');
			Js::push_inline('var STATIC_CROSSDOMAIN = "'.Config::get('materia.urls.static_crossdomain').'";');
			$response = Response::forge(Theme::instance()->render());
		}

		return parent::after($response);
	}

	/**
	 * Uses Materia API's remote_login function to log the user in.
	 *
	 */
	public function action_login()
	{
		// figure out where to send if logged in
		$redirect = Input::get('redirect') ?: Router::get('profile');

		if (Model_User::find_current())
		{
			// already logged in
			Response::redirect($redirect);
		}

		if (Input::method() == 'POST')
		{
			$login = Materia\Api::session_login(Input::post('username'), Input::post('password'));
			if ($login === true)
			{
				// if the location is the profile and they are an author, send them to my-widgets instead
				if (Materia\Api::session_valid('basic_author') == true && $redirect == Router::get('profile'))
				{
					$redirect = 'my-widgets';
				}
				Response::redirect($redirect);
			}
			else
			{
				$msg = \Model_User::check_rate_limiter() ? 'ERROR: Username and/or password incorrect.' : 'Login locked due to too many attempts.';
				Session::set_flash('login_error', $msg);
			}
		}

		$this->theme->get_template()
			->set('title', 'Login')
			->set('page_type', 'login');

		$this->theme->set_partial('content', 'partials/login')
			->set('redirect', urlencode($redirect));

		Css::push_group("login");
	}
	/**
	 * Uses Materia API's remote_logout function to log the user in.
	 *
	 */
	public function action_logout()
	{
		Materia\Api::session_logout();
		Response::redirect(Router::get('login'));
	}

	/**
	 * Displays information about the currently logged-in user
	 *
	 */
	public function action_profile()
	{
		if (Materia\Api::session_valid() !== true)
		{
			Session::set_flash('notice', 'Please log in to view this page.');
			Response::redirect(Router::get('login').'?redirect='.URI::current());
		}

		// to properly fix the date display, we need to provide the raw server date for JS to access
		$server_date  = date_create('now', timezone_open('UTC'))->format('D, d M Y H:i:s');

		Js::push_inline("var DATE = '$server_date'");

		$this->theme->get_template()
			->set('title', 'Profile')
			->set('page_type', 'user profile');

		$this->theme->set_partial('content', 'partials/user/profile')
			->set('me', \Model_User::find_current());

		Css::push_group("profile");
	}

	/**
	 * Displays information about the currently logged-in user
	 *
	 */
	public function action_settings()
	{
		if (Materia\Api::session_valid() !== true)
		{
			Session::set_flash('notice', 'Please log in to view this page.');
			Response::redirect(Router::get('login').'?redirect='.URI::current());
		}

		$this->theme->get_template()
			->set('title', 'Settings')
			->set('page_type', 'user profile settings');

		$this->theme->set_partial('content', 'partials/user/settings')
			->set('me', \Model_User::find_current());

		Css::push_group("profile");
		Js::push_group("settings");
	}

	// TODO: move this to the api
	public function post_update()
	{
		// whitelist input
		$whitelist = ['useGravatar', 'beardMode', 'notify'];
		$set_meta  = [];
		$success   = false;

		if (Materia\Api::session_valid() === true)
		{
			foreach ($whitelist as $property)
			{
				// prop may exist and be boolean(false), so default to null then check against null
				$val = Input::json($property, null);
				if ( ! is_null($val)) $set_meta[$property] = $val;
			}
			if(count($set_meta) > 0)
			{
				$success = Materia\Api::user_update_meta($set_meta);
			}
		}

		$me = \Model_User::find_current();

		$reply = [
			'success' => $success,
			'avatar'  => \Materia\Utils::get_avatar(),
			'meta'    => $me->profile_fields,
		];

		return new Response(json_encode($reply));
	}
}

/* End of file users.php */
