<?php
/**
 * Fuel
 *
 * Fuel is a fast, lightweight, community driven PHP5 framework.
 *
 * @package		Fuel
 * @version		1.0
 * @author		Fuel Development Team
 * @license		MIT License
 * @copyright	2010 Dan Horrigan
 * @link		http://fuelphp.com
 */

$loader = new Autoloader;
$loader->default_path(dirname(__FILE__).'/classes/');

$loader->add_namespaces(array(
	APP_NAMESPACE		=> __DIR__.'/classes/',
));

$loader->register();
return $loader;

/* End of file autoload.php */