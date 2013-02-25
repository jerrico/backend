
# Restrictions

Restrictions allow you to configure the options and things a user can access. Restrictions are checked against whenever you are calling ``can("action")`` to check whether an user is allowed to do something. There can be multiple restrictions per action and they are checked in the given order (top to bottom) when can is requested. Only if none of them restricts the permission is granted.

If no restriction is given the default for that profile is applied ("deny" if not configured specificity).

There are currently various forms of restrictions you can configure for your profile. This doc is meant to explain how to do that and how they act in production.


## BinaryRestriction
A simple "allow deny" switch. Very useful to explicitly permit or deny access to certain profiles. 


## PerTimeRestriction
This Permission checks whether an action has been issued over a certain quota over a given period. For example you might want to restrict the "Free"-Profiles to only "upload_photo" to 10 per week. As said above you can combine multiple restrictions, for example you could say that though a user might be upload 10 photos per 7-day-period, you also restrict it to 3 per 24 hours. Only if both of them have not been exceeded ``can('upload_photo')`` would allow access.


## TotalAmountRestriction
Maybe you want to specify a total count that an action may be performed over the lifetime of the user independent of the time frame. Use this Restriction for to limit that. A classic example would be that a free user can only start the app 30 times and would have to upgrade after.

## LocalAmountRestriction
The LocalAmountRestriciton as well checks against an absolute maximum the user is allowed to do/have. But other than the TotalAmountRestriction it is not looking at the history and calculates all log-entries to figure out how many the user has left, but checks the given amount against this local amount. This is useful if you want to keep track of a certain fluctuative number of local settings (for e.g. active projects or scheduled messages), which changes frequently. It is expected that the developers takes care of the tracking here, but it is still encouraged to record changes via the did-command (though they do not have any influence on this restriction)

## AccountAmountRestriction
This restriction checks against an amount given on the profile data to find out whether the permission is allowed. A classic case for that would be to have credits on the user account and allow an action only if the user has enough credits left to perform the action. Don't forget to specify which item on the account should be checked against. If the item isn't specified on the account, the permission will be denied in any case.


