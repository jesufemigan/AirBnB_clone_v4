#pippet file to configure web_Server

package { 'nginx':
  ensure  => 'present',
}

file { ['/data, /data/web_static', /data/web_static/releases,
	/data/web_static/shared']:
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu'
  recurse => true,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => '<html><head></head><body>Holberton School</body></html>',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/'
}

$nginx_path='/etc/nginx/sites-available/default'
exec { 'nginx config':
  command   => sed -i '/listen 80 default_server/a location /hbnb_static { alias
	  /data/web_static/current/;}' $nginx_path,
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}
