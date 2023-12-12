from django.urls import reverse_lazy
from global_methods import get_categories_list

HOME_ACTIVITIES_OF_ANDROID = {
    "1": "MainActivity",
}

HOME_ACTIVITIES_OF_IOS = {
    "1": "MainActivity",
}

SITE_TABS = [
    {
        'display_name': 'Dashboard',
        'icon': 'home',
        'id': 'admin_dashboard',
        'link_url': reverse_lazy('admin_dashboard'),
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Dashboard',
        'icon': 'home',
        'id': 'vendor_dashboard',
        'link_url': reverse_lazy('vendor_dashboard'),
        'visible': ['vendor'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Categories',
        'icon': 'server',
        'id': 'categories',
        'link_url': '#',
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [
            {
                'display_name': 'Main Categories',
                'id': 'main_categories',
                'link_url': reverse_lazy('list_categories'),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            },
            {
                'display_name': 'Sub Categories',
                'id': 'sub_categories',
                'link_url': reverse_lazy('list_sub_categories'),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            }
        ],
        'type': 'feather'
    },
    {
        'display_name': 'Brands',
        'icon': 'tag',
        'id': 'brands',
        'link_url': reverse_lazy('list_brands'),
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Banners',
        'icon': 'image',
        'id': 'banners',
        'link_url': reverse_lazy('list_banners'),
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Businesses',
        'icon': 'briefcase',
        'id': 'list_business',
        'link_url': "#",
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [
            {
                'display_name': 'All Businesses',
                'id': 'list_business',
                'link_url': reverse_lazy('list_all_businesses'),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            },
            {
                'display_name': 'Claim Request',
                'id': 'claim_business',
                'link_url': reverse_lazy('list_claim_business'),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            }
        ],
        'type': 'feather'
    },
    {
        'display_name': 'Users',
        'icon': 'users',
        'id': 'users',
        'link_url': reverse_lazy('list_users'),
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Discounts',
        'icon': 'percent',
        'id': 'discount',
        'link_url': reverse_lazy('list_trending_discounts'),
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Stories',
        'icon': 'video',
        'id': 'stories',
        'link_url': reverse_lazy('vendor_active_stories'),
        'visible': ['vendor'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Reviews',
        'icon': 'star',
        'id': 'reviews',
        'link_url': reverse_lazy('vendor_reviews'),
        'visible': ['vendor'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Check-In',
        'icon': 'map-pin',
        'id': 'check_in',
        'link_url': reverse_lazy('vendor_active_check_in'),
        'visible': ['vendor'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Voting',
        'icon': 'thumbs-up',
        'id': 'votes',
        'link_url': reverse_lazy('vendor_votes'),
        'visible': ['vendor'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Visitors',
        'icon': 'users',
        'id': 'visitors',
        'link_url': reverse_lazy('vendor_visitors_list'),
        'visible': ['vendor'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Subscription Plans',
        'icon': 'rocket',
        'id': 'plans',
        'link_url': reverse_lazy('list_subscriptions'),
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'fontawesome'
    },
    {
        'display_name': 'Promotions',
        'icon': 'rectangle-ad',
        'id': 'promotions',
        'link_url': reverse_lazy('list_promotions'),
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'fontawesome'
    },
    {
        'display_name': 'Others',
        'icon': 'command',
        'id': 'faqs',
        'link_url': "#",
        'visible': ['admin'],
        'visible_categories': get_categories_list(),
        'active': True,
        'actions': [
            {
                'display_name': 'About Us',
                'id': 'others_about_us',
                'link_url': reverse_lazy("others_about_us"),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            },
            # {
            #     'display_name': 'FAQs',
            #     'id': 'faqs',
            #     'link_url': reverse_lazy('others_faq'),
            #     'visible': ['admin'],
            #     'visible_categories': get_categories_list(),
            #     'active': False
            # },
            {
                'display_name': 'Terms & Condition',
                'id': 'others_terms_and_condition',
                'link_url': reverse_lazy("others_terms_and_condition"),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            },
            {
                'display_name': 'Privacy Policy',
                'id': 'others_privacy_policy',
                'link_url': reverse_lazy("others_privacy_policy"),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            },
            {
                'display_name': 'Disclaimer',
                'id': 'others_disclaimer',
                'link_url': reverse_lazy("others_disclaimer"),
                'visible': ['admin'],
                'visible_categories': get_categories_list(),
                'active': False
            },
        ],
        'type': 'feather'
    },
    {
        'display_name': 'Bookings',
        'icon': 'utensils',
        'id': 'bookings',
        'link_url': reverse_lazy('list_vendor_bookings'),
        'visible': ['vendor'],
        'visible_categories' : ['Restaurant'],
        'active': True,
        'actions': [],
        'type': 'fontawesome'
    },
    {
        'display_name': 'Products',
        'icon': 'shopping-bag',
        'id': 'products',
        'link_url': reverse_lazy('list_vendor_products'),
        'visible': ['vendor'],
        'visible_categories' : ['Products'],
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Services',
        'icon': 'screwdriver-wrench',
        'id': 'service',
        'link_url': reverse_lazy('list_vendor_services'),
        'visible': ['vendor'],
        'visible_categories' : ['Services'],
        'active': True,
        'actions': [],
        'type': 'fontawesome'
    },
    {
        'display_name': 'Services',
        'icon': 'briefcase-medical',
        'id': 'health_care_service',
        'link_url': reverse_lazy('list_vendor_health_care_services'),
        'visible': ['vendor'],
        'visible_categories' : ['Health Care'],
        'active': True,
        'actions': [],
        'type': 'fontawesome'
    },
    {
        'display_name': 'Menus',
        'icon': 'pizza-slice',
        'id': 'menu',
        'link_url': reverse_lazy('list_vendor_menus'),
        'visible': ['vendor'],
        'visible_categories' : ['Restaurant'],
        'active': True,
        'actions': [],
        'type': 'fontawesome'
    },
    {
        'display_name': 'Offers',
        'icon': 'percent',
        'id': 'offers',
        'link_url': reverse_lazy('list_vendor_offers'),
        'visible': ['vendor'],
        'visible_categories' : get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    },
    {
        'display_name': 'Chat',
        'icon': 'message-square',
        'id': 'chat',
        'link_url': reverse_lazy('chat'),
        'visible': ['vendor'],
        'visible_categories' : get_categories_list(),
        'active': True,
        'actions': [],
        'type': 'feather'
    }
]